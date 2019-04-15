from keras.models import Sequential
from keras import layers
from keras.optimizers import Adam
from preprocess2 import generateData

#Loading data from our file
(x_train, y_train), (x_test, y_test) = generateData()

model = Sequential()

#Here we have a Conv1D as our first layer
#If we use a Conv1d as a first layer, we must specify the shape of one patient
model.add(layers.Conv1D(12, 3, activation='relu', input_shape=(12,24)))

#Apply Max Pooling with a windows size of 2
model.add(layers.MaxPooling1D(2))

#Apply a second convolutional layer
model.add(layers.Conv1D(8, 2, activation='relu'))

model.add(layers.GlobalMaxPooling1D())
model.add(layers.Dense(1, activation="sigmoid"))

model.summary()

#Here we use Adam optimizer and a loss funtion of Mean Squared Error
model.compile(optimizer=Adam(lr=1e-4),
              loss='mse',
              metrics=['acc'])

history = model.fit(x_train, y_train,
                    epochs=10,
                    batch_size=128,
                    #validation_split=0.2)
                    validation_data=(x_test, y_test))
