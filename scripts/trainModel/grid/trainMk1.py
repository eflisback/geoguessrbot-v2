from keras.applications import EfficientNetV2L
from keras.models import Sequential
from keras.layers import *
import tensorflow as tf
from keras.optimizers import Adam
from keras.losses import CategoricalCrossentropy
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# Data augmentation
from keras.preprocessing.image import ImageDataGenerator

# Check if GPU is available
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    # Restrict TensorFlow to only allocate 10GB of memory on the first GPU
    try:
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=10240)])
    except RuntimeError as e:
        print(e)

# Load the EfficientNetV2L base model with ImageNet weights, without the top layers
base_model = EfficientNetV2L(weights='imagenet',
                             include_top=False,
                             input_shape=(224, 224, 3))

# Unfreeze some layers of the base model
for layer in base_model.layers[:-20]:
    layer.trainable = False

# Build the complete model by adding custom layers to the base model
complete_model = Sequential([base_model,
                             Conv2D(1024, 3, 1, activation='relu'),
                             BatchNormalization(),
                             GlobalAveragePooling2D(),
                             Dense(1024, activation='relu'),
                             BatchNormalization(),
                             Dropout(0.2),
                             Dense(1024, activation='relu'),
                             BatchNormalization(),
                             Dropout(0.2),
                             Dense(59, activation='softmax')])

# Print the model summary
complete_model.summary()

# Define data directory, batch size, and seed
data_dir = '../../../data/grid/training'
BATCH_SIZE = 24
SEED = 1

# Create data generator for data augmentation
data_gen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)

# Create training dataset
train_dataset = data_gen.flow_from_directory(
    data_dir,
    color_mode='rgb',
    batch_size=BATCH_SIZE,
    target_size=(224, 224),
    shuffle=True,
    subset='training',
    seed=SEED,
    class_mode='categorical'
)

# Create validation dataset
val_dataset = data_gen.flow_from_directory(
    data_dir,
    color_mode='rgb',
    batch_size=BATCH_SIZE,
    target_size=(224, 224),
    shuffle=False,
    subset='validation',
    seed=SEED,
    class_mode='categorical'
)

# Define the metrics
metrics = ['accuracy']

# Compile the model
complete_model.compile(loss=CategoricalCrossentropy(),
                       optimizer=Adam(learning_rate=0.001),
                       metrics=metrics)

# Define early stopping callback
es = EarlyStopping(patience=3, monitor='val_loss')

# Define ReduceLROnPlateau callback
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-6, verbose=1)

# Define ModelCheckpoint callback
model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True, verbose=1)

# Train the model
complete_model.fit(train_dataset, epochs=10, validation_data=val_dataset, callbacks=[es, reduce_lr, model_checkpoint])

# Load the best model weights
complete_model.load_weights('best_model.h5')

# Save the trained model
complete_model.save('GriddaBriddaMk1.h5')
