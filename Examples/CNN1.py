from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop, Adamax
from preprocess import generateData

#Loading data from our file
(x_train, y_train), (x_test, y_test) = generateData()

#Here we specify max number of unique words
max_features = 500
max_len = x_train.shape[1]

#Here we start our Sequential model
model = Sequential()

#First layer
#Embeds data to a unique vector
#Embedding(unique words, output dimension, input_length)
model.add(layers.Embedding(max_features, 64, input_length=max_len))

#Apply a 1D Convolution
#Conv1D(output_features, stride, activation)
model.add(layers.Conv1D(32, 7, activation='relu'))

#Apply Max Pooling with a windows size of 4
model.add(layers.MaxPooling1D(4))

#Apply a second convolutional layer
model.add(layers.Conv1D(4, 2, activation='relu'))

#Global Max Pooling is like a Flatten layer
model.add(layers.GlobalMaxPooling1D())

#THe Nueral Network layer
model.add(layers.Dense(1))

#THis prints the model's arquitecture with some useful info about every layer
model.summary()

#Here we compile the model with it's parameters
model.compile(optimizer=RMSprop(lr=1e-4),
              loss='binary_crossentropy',
              metrics=['acc'])

#Here we actually run the training
history = model.fit(x_train, y_train,
                    epochs=10,
                    batch_size=128,
                    #validation_split=0.2
                    validation_data=(x_test, y_test))

model.evaluate(history)