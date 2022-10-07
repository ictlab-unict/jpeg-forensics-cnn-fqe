import numpy as np
from PIL import Image
import sys
import matplotlib.pyplot as plt
import csv
import os
from os import path
import time
from PIL import ImageFile
import datetime
import subprocess
import pandas as pd
from sklearn import preprocessing
from keras.optimizers import SGD
from sklearn.metrics import accuracy_score
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten,Dropout, BatchNormalization, Activation
from keras.regularizers import l2
from keras.callbacks import LearningRateScheduler
from tensorflow import keras



def get_dct_coeffs_distribution(path,width,height):
    #leggo valori DCT dal file (senza aprire l'immagine ed evitando l'errore di truncation)
    #restituisce le 64 distribuzioni scorrendo colonna per colonna (1,1),(2,1)......(8,1),(2,1),(2,2)
    p = subprocess.Popen(["./jpeg " + path],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    out, info_jpeg = p.communicate()
    executable = os.access('jpeg', os.X_OK)
    if not executable:
        print("Permission denied on jpeg file. jpeg file must be executable to work!")
        sys.exit(0)
    coefficents = np.array(out.splitlines()).astype('int')


    #ottengo larghezza e altezza massima dei blocchi 8X8
    while (width%8) !=0:
        width-=1
    while (height%8) !=0:
        height-=1

    #ottengo le distribuzioni dei 64 coefficienti
    distributions = np.zeros((int(width*height/64), 64))
    n_dist=0

    for i in range(0, len(coefficents), 64):
        if ((i+64) <= (width * height)):
            dist=np.reshape(coefficents[i:i + 64],(8,8))
            dist=np.transpose(dist)
            dist=np.reshape(dist,(1,-1))
            distributions[n_dist]=dist
            n_dist+=1
    return distributions


def coeff_to_zigzag_index(coeff):
    #ordinamento colonna per colonna
    map=[]
    map.append(0)
    map.append(8)
    map.append(1)
    map.append(2)
    map.append(9)
    map.append(16)
    map.append(24)
    map.append(17)
    map.append(10)
    map.append(3)
    map.append(4)
    map.append(11)
    map.append(18)
    map.append(25)
    map.append(32)

    return map[coeff]


if __name__ == '__main__':

    img = '128_128.jpg'
    # img='4288_2848.jpg'
    number_nets = 2

    AC_nets_mixed = {}
    DC_nets_mixed = {}
    for q2 in range(1, 23):
        AC_nets_mixed[q2] = {}
        DC_nets_mixed[q2] = {}
        for single_net in range(0, number_nets):
            AC_nets_mixed[q2][single_net] = keras.models.load_model(
                'net_models/' + str(number_nets) + '/' + str(q2) + '/model_' + str(single_net) + '.h5', compile=False)
            DC_nets_mixed[q2][single_net] = keras.models.load_model(
                'net_models/' + str(number_nets) + '/' + str(q2) + '/DC_model_' + str(single_net) + '.h5',
                compile=False)



    # apro il file e ne estraggo le dimensioni e l'ultima tabella di quantizzazione
    _img = Image.open(img)
    # tabella di quantizzazione in zig-zag order
    Q2 = _img.quantization[0]
    width, height = _img.size
    _img.close()
    coeffs_distribution = get_dct_coeffs_distribution(img, width, height)

    # massimo q2 presente sul training set
    maximum_q2 = 22


    # preparo le strutture dati per le distribuzioni, una per ogni q2
    distributions = {}
    for q2 in range(1, maximum_q2 + 1):
        distributions[q2] = []

    # range per la generazione degli istogrammi
    _range = np.array(range(0, 1026)) - 0.5

    # per i primi 15 coeff
    for coeff in range(0, 15):
        # indice coefficiente
        dct_coeff = coeff + 1

        # ottengo l'indice in ordinamento zigzag
        zig_zag_coeff = coeff_to_zigzag_index(coeff)

        # ed il relativo q2 (utilizzo coeff come index perche Q2 e gia in zig-zag order)
        q2 = Q2[coeff]

        # moltiplico per le distribuzioni (simulando la IDCT ed ottenere i valori dul dominio spaziale senza errore di truncate)
        data = coeffs_distribution[:, zig_zag_coeff]
        data = data * q2

        # genero istogrammi associati ai coefficenti con valore assoluto
        data = np.absolute(data)
        hist, _ = np.histogram(data, _range)

        hist = hist.astype(float)

        # aggiungo il DCT analizzato come primo valore
        hist = np.insert(hist, 0, dct_coeff)

        distributions[q2].append(hist)

    predictions=np.zeros(15)
    for q2 in range(1, 23):
        if(len(distributions[q2])>0):
            for row in distributions[q2]:

                dct_coeff_query = int(row[0])
                hist_query = np.array(row[1:][::q2]).astype('int')
                if dct_coeff_query == 1:
                    net=DC_nets_mixed[q2][single_net]
                else:
                    net=AC_nets_mixed[q2][single_net]

                X_test = []
                X_test.append(hist_query)
                X_test_normalized = preprocessing.normalize(np.array(X_test), norm='l1', axis=1)
                tot_test_examples = X_test_normalized.shape[0]
                height = int(np.ceil(X_test_normalized.shape[1]))
                Xtest_reshaped = X_test_normalized.reshape(tot_test_examples, 1, height, 1)
                softmax = {}
                for single_net in range(0, number_nets):
                    if single_net == 0:
                        softmax = net.predict(Xtest_reshaped)[0]
                    else:
                        softmax = softmax + net.predict(Xtest_reshaped)[0]

                mean_softmax = softmax / number_nets
                q1_predicted = np.argmax(mean_softmax) + 1
                predictions[dct_coeff_query - 1] = q1_predicted
    print(predictions)
    sys.exit(0)










