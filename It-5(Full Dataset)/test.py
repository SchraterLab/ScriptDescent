import pandas as pd
import math
import numpy as np
import os
import h5py
from utils import data_load, plot_example
from keras.models import Sequential, Model, load_model
from keras.initializers import Initializer, RandomNormal, RandomUniform
from keras.layers import Input, Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.optimizers import SGD, Adadelta
from keras.constraints import maxnorm

cwd = os.getcwd()
fontsPath = cwd+"/fonts"

fonts = []
for root, dirs, files in os.walk(fontsPath):
	for e in files:	
		fonts.append(e.split(".")[0])

print(fonts)

X_test,X_train,Y_test,Y_train,idx_to_label,label_to_idx = data_load(0.7,fonts)

def get_model(target_shape=153):
	model_name = "model_with_target_"+str(target_shape)+".h5"

	if os.path.exists(model_name):
		return load_model(model_name)

	else:
		X_input = Input(shape=(20,20,1,))

		conv = Conv2D(32, (3, 3), activation='relu', padding='same')(X_input)

		pool = MaxPooling2D(pool_size=(2, 2))(conv)

		dropout = Dropout(0.5)(pool)

		flat = Flatten()(dropout)

		dense1 = Dense(512, activation='relu', kernel_constraint=maxnorm(3))(flat)

		dropout = Dropout(0.5)(dense1)

		dense2 = Dense(target_shape, activation='softmax')(dropout)

		model = Model(inputs=X_input, outputs=dense2)

		sgd = SGD(lr=0.1)

		model.compile(loss = 'categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
		
		# Save the model
		model.save(model_name)
		return(model)

print(len(X_train),len(Y_train))
model = get_model(len(idx_to_label))
model.fit(X_train, Y_train, epochs=10, batch_size=32)
score = model.evaluate(X_test, Y_test, show_accuracy = True, verbose = 0)
print("Test score: ", score[0])
print("Test accuracy: ", score[1])
