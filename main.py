"""
main.py
Description:
Input:
Output:
Author: Fangqi Zhu
Affiliation: University of Texas at Arlington
Last Modified: 05/15/2018
"""

import numpy as np
import matplotlib.pyplot as plt

from load_util import load_spec_data
from load_util import MFCC_vocal
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop


"""
Extract short time fourier transform (STFT) coefficients

Remark: 
1. Scipy and MATLAB use different FFT libraries. Scipy uses lapack, while MATLAB uses FFTW. 
These libraries use different algorithms and produce slightly different results.
2. The dimension of the S matrix so absolute different, please keep consensus for usage.
3. The loading part will load the Spectrogram matrix extracted from MATLAB function spectrogram.m

"""


param_STFT = load_spec_data()

S_normal_a2 = param_STFT["S_normal_a2"]
S_abnormal_a2 = param_STFT["S_abnormal_a2"]
S_normal_i1 = param_STFT["S_normal_i1"]
S_abnormal_i1 = param_STFT["S_abnormal_i1"]



"""
MFCC features
"""

param_MFCC = MFCC_vocal()

mfcc_normal_a2 = param_MFCC["mfcc_normal_a2"]
mfcc_abnormal_a2 = param_MFCC["mfcc_abnormal_a2"]
mfcc_normal_i1 = param_MFCC["mfcc_normal_i1"]
mfcc_abnormal_i1 = param_MFCC["mfcc_abnormal_i1"]
fbank_normal_a2 = param_MFCC["fbank_normal_a2"]
fbank_abnormal_a2 = param_MFCC["fbank_abnormal_a2"]
fbank_normal_i1 = param_MFCC["fbank_normal_i1"]
fbank_abnormal_i1 = param_MFCC["fbank_abnormal_i1"]

print(mfcc_normal_a2.shape, '\n',
      mfcc_abnormal_a2.shape, '\n',
      mfcc_normal_i1.shape, '\n',
      mfcc_abnormal_i1.shape, '\n',
      fbank_normal_a2.shape, '\n',
      fbank_abnormal_a2.shape, '\n',
      fbank_normal_i1.shape, '\n',
      fbank_abnormal_i1.shape
      )

# training data
X = np.concatenate((mfcc_normal_a2, mfcc_abnormal_a2))
X = X[:,:24]
# annotating labels
y = np.concatenate((np.ones((mfcc_normal_a2.shape[0], 1)), -np.ones((mfcc_abnormal_a2.shape[0], 1))))


"""
pass the arrays as an iterable (a tuple or list), thus the correct syntax is np.concatenate((...)) for 1-D array

"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
X_train = X_train[:, :, np.newaxis]         # numpy newaxis: add a new dimension
X_test = X_test[:, :, np.newaxis]
y_train = np.squeeze(y_train)               # numpy squeeze: reduce a dimension
y_test = np.squeeze(y_test)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)


# Model Building and Parameters Setup
length = 13
model = Sequential()
model.add(LSTM(32, input_shape=(length, 1), return_sequences=False))
model.add(Dropout(0.4))
model.add(Dense(1))
model.add(Activation('tanh'))
optimizer = RMSprop(lr=0.005, clipvalue=1.)


# Training and validation
model.compile(optimizer = optimizer,
              loss='binary_crossentropy',
              metrics=['acc'])

history = model.fit(X_train, y_train,
                    epochs=30,
                    batch_size=32,
                    validation_split=0.25)

results = model.evaluate(X_test, y_test)
print('test loss: ', results[0], '\n',
      'test accuracy: ', results[1])

# plot results

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, linestyle = '-.', label='Training acc')
plt.plot(epochs, val_acc, linestyle = '-', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, linestyle = '-.', label='Training loss')
plt.plot(epochs, val_loss, linestyle = '-', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
































