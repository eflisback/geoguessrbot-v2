"""
Training script for fifth model (unfinished)

This model hasn't yet been trained due to a few bugs in my script which I haven't yet solved. This script introduces
new technologies such as reducing learning rate on plateaus. The data augmentation has also been improved.
"""

from keras.applications import EfficientNetB3
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

# Load the EfficientNetB3 base model with ImageNet weights, without the top layers
base_model = EfficientNetB3(weights='imagenet',
                            include_top=False,
                            input_shape=(224, 224, 3))

# Unfreeze some layers of the base model
for layer in base_model.layers[:-10]:
    layer.trainable = False

# Build the complete model by adding custom layers to the base model
complete_model = Sequential([base_model,
                             Conv2D(1024, 3, 1, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
                             BatchNormalization(),
                             GlobalAveragePooling2D(),
                             Dense(1024, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
                             BatchNormalization(),
                             Dropout(0.5),
                             Dense(1024, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
                             BatchNormalization(),
                             Dropout(0.5),
                             Dense(37, activation='softmax')])

# Print the model summary
complete_model.summary()

# Define data directory, batch size, and seed
data_dir = '../../../data/countries/training/224x224_balanced'
BATCH_SIZE = 8
SEED = 1

# Create data generator for data augmentation
data_gen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
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
                       optimizer=Adam(learning_rate=1e-4),
                       metrics=metrics)

# Define early stopping callback
es = EarlyStopping(patience=5, monitor='val_loss')

# Define ReduceLROnPlateau callback
# reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6, verbose=1)

# Define ModelCheckpoint callback
model_checkpoint = ModelCheckpoint('./best_model.h5', monitor='val_loss', save_best_only=True, verbose=1)

# Train the model
complete_model.fit(train_dataset, epochs=50, validation_data=val_dataset, callbacks=[es, model_checkpoint])

# Load the best model weights
complete_model.load_weights('best_model.h5')

# Save the trained model
complete_model.save('HittaBrittaMk5.h5')

