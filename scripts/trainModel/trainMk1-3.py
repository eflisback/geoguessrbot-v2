# Training script for first fine-tuned based HittaBritta models, which reached about 45% accuracy in testing

import keras.utils
from keras.applications import EfficientNetV2L
from keras.models import Sequential
from keras.layers import *
import tensorflow as tf
from keras.optimizers import Adam
from keras.losses import CategoricalCrossentropy
from keras.callbacks import EarlyStopping

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

# Freeze the layers of the base model
for layer in base_model.layers:
    layer.trainable = False

# Build the complete model by adding custom layers to the base model
complete_model = Sequential([base_model,
                             Conv2D(1024, 3, 1, activation='relu'),
                             GlobalAveragePooling2D(),
                             Dense(1024, activation='relu'),
                             Dropout(0.2),
                             Dense(1024, activation='relu'),
                             Dropout(0.2),
                             Dense(37, activation='softmax')])

# Print the model summary
complete_model.summary()

# Define data directory, batch size, and seed
data_dir = '../../data/training/224x224_balanced'
BATCH_SIZE = 24
SEED = 1

# Create training dataset
train_dataset = keras.utils.image_dataset_from_directory(
    data_dir,
    color_mode='rgb',
    batch_size=BATCH_SIZE,
    image_size=(224, 224),
    shuffle=True,
    validation_split=0.2,
    subset='training',
    seed=SEED,
    label_mode='categorical'
)

# Create validation dataset
val_dataset = keras.utils.image_dataset_from_directory(
    data_dir,
    color_mode='rgb',
    batch_size=BATCH_SIZE,
    image_size=(224, 224),
    shuffle=False,
    validation_split=0.2,
    subset='validation',
    seed=SEED,
    label_mode='categorical'
)

# Prefetch data for performance improvement
train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
val_dataset = val_dataset.prefetch(tf.data.AUTOTUNE)

# Define the metrics
metrics = ['accuracy']

# Compile the model
complete_model.compile(loss=CategoricalCrossentropy(),
                       optimizer=Adam(learning_rate=0.003),
                       metrics=metrics)

# Define early stopping callback
es = EarlyStopping(patience=3, monitor='val_loss')

# Train the model
complete_model.fit(train_dataset, epochs=10, validation_data=val_dataset, callbacks=[es])

# Save the trained model
complete_model.save('HittaBrittaMk4.h5')
