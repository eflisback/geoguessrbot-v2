import keras.utils
from keras.applications import EfficientNetV2L
from keras.models import Sequential
from keras.layers import *
import tensorflow as tf
from keras.optimizers import Adam
from keras.losses import CategoricalCrossentropy
from keras.callbacks import EarlyStopping


gpus = tf.config.list_physical_devices('GPU')
if gpus:
    # Restrict TensorFlow to only allocate 10GB of memory on the first GPU
    try:
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=10240)])
    except RuntimeError as e:
        print(e)


base_model = EfficientNetV2L(weights='imagenet',
                             include_top=False,
                             input_shape=(224, 224, 3))

for layer in base_model.layers:
    layer.trainable = False

complete_model = Sequential([base_model,
                             Conv2D(1024, 3, 1, activation='relu'),
                             GlobalAveragePooling2D(),
                             Dense(1024, activation='relu'),
                             Dropout(0.2),
                             Dense(1024, activation='relu'),
                             Dropout(0.2),
                             Dense(37, activation='softmax')])

complete_model.summary()

data_dir = '../data/training/224x224'
BATCH_SIZE = 16
SEED = 1

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

train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
val_dataset = val_dataset.prefetch(tf.data.AUTOTUNE)

metrics = ['accuracy']

complete_model.compile(loss=CategoricalCrossentropy(),
                       optimizer=Adam(learning_rate=0.001),
                       metrics=metrics)

es = EarlyStopping(patience=3, monitor='val_loss')

complete_model.fit(train_dataset, epochs=10, validation_data=val_dataset, callbacks=[es])

complete_model.save('test.h5')
