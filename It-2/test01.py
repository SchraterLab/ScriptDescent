import pandas as pd
import math
import numpy as np
import os
import glob

cwd = os.getcwd()
fontsPath = cwd+"/fonts"

data = pd.read_csv(fontsPath+"/AGENCY.csv")
# allFiles = glob.glob(fontsPath + "/*.csv")
# fontList = []
#
# for file_ in allFiles:
#     df = pd.read_csv(file_,index_col=None, header=0)
#     fontList.append(df)

# print(fontList)



X = data.iloc[:,12:].values
Y = data['m_label'].values

splitpoint = math.floor(len(X)*0.7)

X_train = X[:splitpoint]
X_test = X[splitpoint:]

Y_train = Y[:splitpoint]
Y_test = Y[splitpoint:]

X_train = np.reshape(X_train,(-1,20,20,1))
print(X_train.shape)
print(len(X_train))

from keras.models import Sequential, Model
from keras.layers import Input, Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.optimizers import SGD
from keras.constraints import maxnorm

#1.check if reshaping is not affecting the content
#2.create a mapping for the labels (Y)

# Input shape of each image
X_input = Input(shape=(20,20,1,))


conv = Conv2D(32, (3, 3), activation='relu', padding='same')(X_input)

pool = MaxPooling2D(pool_size=(2, 2))(conv)

flat = Flatten()(pool)

dense1 = Dense(512, activation='relu',  kernel_constraint=maxnorm(3))(flat)

dropout = Dropout(0.5)(dense1)

dense2 = Dense(153, activation='softmax')(dropout)

model = Model(inputs=X_input, outputs=dense2)

model.compile(loss = 'categorical_crossentropy', optimizer=SGD(lr=0.01), metrics=['accuracy'])
model.fit(X_train, Y_train, epochs=10, batch_size=32)

import h5py
# Save the model
model.save('Trained_model.h5')
