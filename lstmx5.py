#!/usr/bin/python

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import matplotlib.pyplot as plt

# import keras network libraries
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, GRU, Conv1D, Dropout, Reshape, MaxPooling1D, Flatten, TimeDistributed, Activation, ConvLSTM2D, Conv3D
from keras.layers.normalization import BatchNormalization
import keras

import pandas as pd
pd.core.common.is_list_like=pd.api.types.is_list_like
from pandas import DataFrame
import pandas_datareader.data as web

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

import datetime 
import os,sys

def do_main(argv):
    stock_dataset=''
    if(len(argv)>=3 and argv[2]=='-d'):
        stock=argv[1]
        now_time = datetime.datetime.now()
        past_five_pm=now_time.replace(hour=18, minute=0, second=0, microsecond=0)

        weekno=datetime.datetime.today().weekday()

        stock_dataset = web.DataReader(argv[1],'iex', datetime.datetime(datetime.datetime.now().year - 5, datetime.datetime.now().month , datetime.datetime.now().day), datetime.datetime.now() + datetime.timedelta(days=1))
        stock_dataset['Name']=stock
        stock_dataset.to_csv('./stocks/'+argv[1]+'_data.csv')
        
        if(now_time>=past_five_pm and weekno<5):
            #get the last value padding ohlcv
            current=web.get_last_iex(stock)[0][0]
			
            temphigh=stock_dataset['close'][len(stock_dataset)-1]
            templow=stock_dataset['close'][len(stock_dataset)-1]
            tempvol=int(stock_dataset['volume'][len(stock_dataset)-1])
            previous_close=stock_dataset['close'][len(stock_dataset)-1]
            current_date=datetime.datetime.today().strftime('%Y-%m-%d')


            if(current>temphigh):
                temphigh=current
            if(templow>current):
                templow=current

            with open(os.path.join('.','stocks',stock+'_data.csv'), 'a') as f:
                f.write( '%s,%0.2f,%0.2f,%0.2f,%0.2f,%d,%s\n'%(current_date, previous_close, temphigh, templow, current, tempvol, stock))

            stock_dataset = pd.read_csv('./stocks/'+argv[1]+'_data.csv')

    else:
        stock_dataset = pd.read_csv('./stocks/'+argv[1]+'_data.csv')

    #close_scaler = MinMaxScaler(feature_range=(0,1))
    #y_scaler = MinMaxScaler(feature_range=(0,1))

    stock_dataset_close=stock_dataset['close']
    stock_dataset_high=stock_dataset['high']
    stock_dataset_low=stock_dataset['low']
    stock_dataset_open=stock_dataset['open']
    stock_dataset_volume=stock_dataset['volume']

    window_size = 10

    X = []
    y = []

    for i in range(window_size, len(stock_dataset_close)):
        #X.append(close_scaler.fit_transform([stock_dataset_close[i - window_size:i], stock_dataset_high[i - window_size:i], stock_dataset_low[i - window_size:i], stock_dataset_open[i - window_size:i], stock_dataset_volume[i - window_size:i]]))
        X.append([stock_dataset_close[i - window_size:i], stock_dataset_high[i - window_size:i], stock_dataset_low[i - window_size:i], stock_dataset_open[i - window_size:i], stock_dataset_volume[i - window_size:i]])
        y.append([stock_dataset_close[i]])


    #X.append(close_scaler.fit_transform([stock_dataset_close[len(stock_dataset_close)-window_size:], stock_dataset_high[len(stock_dataset_close)-window_size:], stock_dataset_low[len(stock_dataset_close)-window_size:], stock_dataset_open[len(stock_dataset_close)-window_size:], stock_dataset_volume[len(stock_dataset_close)-window_size:]]))
    X.append([stock_dataset_close[len(stock_dataset_close)-window_size:], stock_dataset_high[len(stock_dataset_close)-window_size:], stock_dataset_low[len(stock_dataset_close)-window_size:], stock_dataset_open[len(stock_dataset_close)-window_size:], stock_dataset_volume[len(stock_dataset_close)-window_size:]])

    #y_train=np.asarray(y)
    #y_train=y_scaler.fit_transform(y)
    y_train = np.asarray(y)
    X=np.asarray(X)

    X_train=X[:-1,]
    X_test=X[-1:,]

    X_train = np.asarray(np.reshape(X_train, (X_train.shape[0], window_size, 5)))
    X_test = np.asarray(np.reshape(X_test, (X_test.shape[0], window_size, 5)))

    # NOTE: to use keras's RNN LSTM module our input must be reshaped to [samples, window size, stepsize] 
    #X_train = np.asarray(np.reshape(X_train, (X_train.shape[0], window_size, 5)))
    #X_test = np.asarray(np.reshape(X_test, (X_test.shape[0], window_size, 5)))

    # start with fixed random seed
    np.random.seed(0)
    #hidden=24

    # Build an RNN to perform regression on our time series input/output data
    model = Sequential()
    model.add(LSTM(128, input_shape=(window_size, 5), return_sequences=True))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(32))
    model.add(Dense(16))
    model.add(Dense(1))

    optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

    # compile the model
    model.compile(loss='mean_squared_error', optimizer=optimizer)

    model.fit(X_train, y_train, epochs=500, batch_size=256, verbose=1)

    model.summary()

    # generate predictions for training
    test_predict = model.predict(X_test)

    print(str(test_predict))

    #prediction=y_scaler.inverse_transform(test_predict)[0][0]
    prediction=test_predict[0][0]

    print("Prediction %s: %f vs %f"%(argv[1], prediction, stock_dataset['close'][len(stock_dataset)-1]))

    if(prediction>stock_dataset['close'][len(stock_dataset)-1]):
        return True
    else:
        return False

if __name__ == "__main__":
    sys.exit(0 if do_main(sys.argv)==True else 1)
