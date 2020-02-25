import keras.backend as K
import numpy as np

from keras.models import Model, load_model
from keras.layers import Input, Activation, Dense, Flatten
from keras.layers.merge import add, multiply, concatenate
from keras.layers.convolutional import Conv2D
from keras.layers.normalization import BatchNormalization
from keras.losses import mean_squared_error
from keras.regularizers import l2
from keras.optimizers import SGD

from copy import deepcopy as cp
from reversiModule import *

def BN(x): return BatchNormalization(axis = 1)(x)

def ReLU(x): return Activation("relu")(x)

def SoftMax(x): return Activation("softmax")(x)

def conv(x, size, cnt, reg, form = "channels_first"):
    return Conv2D(kernel_size = size, filters = cnt,
               padding = "same", data_format = form,
               kernel_regularizer = l2(reg))(x)

def BRC(x, size, cnt, reg):
    return conv(ReLU(BN(x)), size, cnt, reg)

def flat(x): return Flatten()(x)

class Controller:
    def __init__(self):
        self.c = 0.01
        self.m = 0.9
        self.depth = 13

class ReversiModel:
    def __init__(self, mode = None):
        self.model = None
        self.digest = None
        self.param = Controller()
        if mode is None:
            self.build()
            self.compile()
        else:
            self.model = load_model(
                'reversi_ai_model.h5',
                custom_objects={
                    'loss_p': loss_p,
                    'loss_v': loss_v
                }
            )

    def save(self):
        self.model.save('reversi_ai_model.h5')

    def build(self):
        c = self.param.c
        in_x1 = Input((1, 8, 8))
        in_x2 = Input((1, 8, 8))

        x1 = BRC(in_x1, 3, 16, c)
        x2 = BRC(in_x2, 3, 16, c)
        x = multiply([x1, x2])

        for _ in range(self.param.depth):
            x = self.resBlock(x)

        self.model = Model([in_x1, in_x2],
                           [self.policy_head(x, in_x2),
                            self.value_head(x)],
                           name = "reversi_model")

    def resBlock(self, x):
        c = self.param.c
        return add([x, BRC((BRC(x, 3, 16, c)), 3, 16, c)])

    def policy_head(self, x, mapping):
        c = self.param.c
        '''
        return Dense(64, name = "policy_out",
                     activation = "softmax",
                     kernel_regularizer = l2(c)
                     )(flat(add([mapping, ReLU(BN(BRC(x, 1, 2, c)))])))
        '''
        return SoftMax(add(
            [flat(mapping),
             Dense(64, name = "policy_out",
                   kernel_regularizer = l2(c)
                   )(flat(ReLU(BN(BRC(x, 1, 2, c)))))]))

    def value_head(self, x):
        c = self.param.c
        return Dense(1, name = "value_out",
                     activation = "tanh",
                     kernel_regularizer = l2(c)
                     )(Dense(64, activation="relu",
                             kernel_regularizer=l2(c)
                             )(flat(ReLU(BN(BRC(x, 1, 1, c))))))

    def compile(self):
        optimizer = SGD(lr = 1e-2, momentum = self.param.m)
        self.model.compile(loss = [loss_p, loss_v], optimizer = optimizer)

    def train(self, x_train, y_train):
        self.model.fit(x_train, y_train)

def loss_p(pi, p):
    return K.sum(-pi * K.log(p + K.epsilon()), axis = -1)

def loss_v(z, v):
    return 10 * mean_squared_error(z, v)

if __name__ == "__main__":
    ReversiModel().save()
    '''
    x_train = [getInput(cp(initialBoard), 'black')]
    y_train = [np.array(np.zeros(64)).reshape(1, 64), np.array([0])]
    model.train(x_train, y_train)
    '''