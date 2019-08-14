from keras import Sequential
from keras.layers import Conv3D, MaxPooling3D, Flatten, TimeDistributed, LSTM, Dropout, Dense, BatchNormalization
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import OneHotEncoder
import numpy as np

import os

input_dir_list = [
    # 'F:/indexPen/csv/ya_0',
    # 'F:/indexPen/csv/ya_1',
    # 'F:/indexPen/csv/ya_3',
    #
    # 'F:/indexPen/csv/zl_0',
    # 'F:/indexPen/csv/zl_1',
    # 'F:/indexPen/csv/zl_3',
    #
    'F:/indexPen/csv/zy_0',
    'F:/indexPen/csv/zy_1',
    'F:/indexPen/csv/zy_2',
    'F:/indexPen/csv/zy_3'
]

X = None
Y = None
for input_dir in input_dir_list:
    data = np.load(os.path.join(input_dir, 'intervaled_3D.npy'))
    label_array = np.load(os.path.join(input_dir, 'label_array.npy'))

    # put in the data
    if X is None:
        X = data
    else:
        X = np.concatenate((X, data))

    if Y is None:
        Y = label_array
    else:
        Y = np.concatenate((Y, label_array))

# Onehot encode Y ############################################
onehotencoder = OneHotEncoder(categories='auto')
Y = onehotencoder.fit_transform(np.expand_dims(Y, axis=1)).toarray()

# Separate train and test
test_ratio = 0.2

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10, random_state=int(12))

# Build the RNN ###############################################

# input shape = (samples, num_timesteps, x_dim, y_xim, channels)

# Conv structure #####################
# cnn = Sequential()
# cnn.add(Conv3D(filter=16, kernel_size=(3, 3), data_format='channels_last', input_shape=(100, 100, 100, 1),
#                activation='relu'))
# cnn.add(MaxPooling3D(pool_size=(2, 2, 2)))
# cnn.add(Flatten())
######################################

model = Sequential()
model.add(
    TimeDistributed(Conv3D(filters=16, kernel_size=(3, 3, 3), data_format='channels_first', input_shape=(1, 20, 20, 20),
                           activation='relu'), input_shape=(75, 1, 20, 20, 20)))
model.add(TimeDistributed(BatchNormalization()))
model.add(TimeDistributed(MaxPooling3D(pool_size=(2, 2, 2))))
model.add(TimeDistributed(Flatten()))

model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(rate=0.5))

model.add(Dense(5, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, Y_train, validation_data=(X_test, Y_test), shuffle=True, epochs=500,
                    batch_size=60)
