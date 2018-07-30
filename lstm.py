#!/usr/bin/python

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import matplotlib.pyplot as plt

# import keras network libraries
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, GRU
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
        past_five_pm=now_time.replace(hour=16, minute=0, second=0, microsecond=0)

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

    dataset=stock_dataset['close']

    x_scaler = MinMaxScaler(feature_range=(0, 1))
    y_scaler = MinMaxScaler(feature_range=(0, 1))

    window_size = 10

    X = []
    y = []

    for i in range(window_size, len(dataset)):
        X.append(dataset[i - window_size:i])
        y.append([dataset[i]])


    X.append(dataset[len(dataset)-window_size:])

    X=np.asarray(X)
    y=np.asarray(y)

    X=x_scaler.fit_transform(X)
    y_train=y_scaler.fit_transform(y)


    X_train=X[:-1,]
    X_test=X[-1:,]


    # NOTE: to use keras's RNN LSTM module our input must be reshaped to [samples, window size, stepsize] 
    X_train = np.asarray(np.reshape(X_train, (X_train.shape[0], window_size, 1)))
    X_test = np.asarray(np.reshape(X_test, (X_test.shape[0], window_size, 1)))

    # start with fixed random seed
    np.random.seed(0)

    # Build an RNN to perform regression on our time series input/output data
    model = Sequential()
    model.add(LSTM(128, input_shape=(window_size, 1), return_sequences=True))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(32))
    model.add(Dense(16))
    model.add(Dense(1))

    optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

    model.summary()

    # compile the model
    model.compile(loss='mean_squared_error', optimizer=optimizer)

    model.fit(X_train, y_train, epochs=500, batch_size=256, verbose=1)

    # generate predictions for training
    test_predict = model.predict(X_test)

    prediction=y_scaler.inverse_transform(test_predict)[0][0]

    dataset=np.asarray(dataset)

    history=dataset[-1]

    print("Prediction %s: %f vs Last Value: %f"%(argv[1], prediction, history))

    if(prediction>history):
        return True
    else:
        return False

if __name__ == "__main__":
    sys.exit(0 if do_main(sys.argv)==True else 1)
