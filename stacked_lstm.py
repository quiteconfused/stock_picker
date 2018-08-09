#!/usr/bin/python

import warnings
warnings.filterwarnings("ignore")

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Conv1D, Flatten, Reshape, GlobalMaxPooling3D, Conv1D, Conv2D, Conv3D, Flatten, Reshape, GlobalMaxPooling3D, TimeDistributed, ConvLSTM2D
from keras.layers.normalization import BatchNormalization
import numpy as np
import json
import os, sys
from keras.optimizers import SGD
from lstm import do_main
import datetime
from Robinhood import Robinhood

from sklearn.preprocessing import MinMaxScaler


def main(argv):
    try:
        spy={}
        tickers=""
        MAX_SIZE=10
        SHUFFLE_STOCKS=False
        batch_size=256
        epochs=200
        minimum_acc=0.03
        MAX_ARGS=11
        USE_ADAM=False
        predownloaded_csv=''
        num_of_years=1
        test=0


        tickers = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADS', 'ADSK', 'AEE', 'AEP', 'AES', 'AET', 'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'ALXN', 'AMAT', 'AMD', 'AME', 'AMG', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANDV', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'APC', 'APD', 'APH', 'APTV', 'ARE', 'ARNC', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BAX', 'BBT', 'BBY', 'BDX', 'BEN', 'BF.B', 'BHF', 'BHGE', 'BIIB', 'BK', 'BKNG', 'BLK', 'BLL', 'BMY', 'BR', 'BRK.B', 'BSX', 'BWA', 'BXP', 'C', 'CA', 'CAG', 'CAH', 'CAT', 'CB', 'CBOE', 'CBRE', 'CBS', 'CCI', 'CCL', 'CDNS', 'CELG', 'CERN', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COG', 'COL', 'COO', 'COP', 'COST', 'COTY', 'CPB', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTL', 'CTSH', 'CTXS', 'CVS', 'CVX', 'CXO', 'D', 'DAL', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCK', 'DISH', 'DLR', 'DLTR', 'DOV', 'DPS', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DWDP', 'DXC', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'EOG', 'EQIX', 'EQR', 'EQT', 'ES', 'ESRX', 'ESS', 'ETFC', 'ETN', 'ETR', 'EVHC', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FAST', 'FB', 'FBHS', 'FCX', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FL', 'FLIR', 'FLR', 'FLS', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRT', 'FTI', 'FTV', 'GD', 'GE', 'GGP', 'GILD', 'GIS', 'GLW', 'GM', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GPS', 'GRMN', 'GS', 'GT', 'GWW', 'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HCP', 'HD', 'HES', 'HFC', 'HIG', 'HII', 'HLT', 'HOG', 'HOLX', 'HON', 'HP', 'HPE', 'HPQ', 'HRB', 'HRL', 'HRS', 'HSIC', 'HST', 'HSY', 'HUM', 'IBM', 'ICE', 'IDXX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'JBHT', 'JCI', 'JEC', 'JEF', 'JNJ', 'JNPR', 'JPM', 'JWN', 'K', 'KEY', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KORS', 'KR', 'KSS', 'KSU', 'L', 'LB', 'LEG', 'LEN', 'LH', 'LKQ', 'LLL', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUV', 'LYB', 'M', 'MA', 'MAA', 'MAC', 'MAR', 'MAS', 'MAT', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'MYL', 'NBL', 'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE', 'NKTR', 'NLSN', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NWL', 'NWS', 'NWSA', 'O', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY', 'PAYX', 'PBCT', 'PCAR', 'PCG', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PX', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RHT', 'RJF', 'RL', 'RMD', 'ROK', 'ROP', 'ROST', 'RSG', 'RTN', 'SBAC', 'SBUX', 'SCG', 'SCHW', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB', 'SLG', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRCL', 'SRE', 'STI', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TDG', 'TEL', 'TGT', 'TIF', 'TJX', 'TMK', 'TMO', 'TPR', 'TRIP', 'TROW', 'TRV', 'TSCO', 'TSN', 'TSS', 'TTWO', 'TWTR', 'TXN', 'TXT', 'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNM', 'UNP', 'UPS', 'URI', 'USB', 'UTX', 'V', 'VAR', 'VFC', 'VIAB', 'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VZ', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WLTW', 'WM', 'WMB', 'WMT', 'WRK', 'WU', 'WY', 'WYNN', 'XEC', 'XEL', 'XL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL', 'YUM', 'ZBH', 'ZION', 'ZTS']

        if(len(argv)<=MAX_ARGS and len(argv)>=2):
            for argument in argv:

                if(argument.startswith('-m=')):
                    minimum_acc=int(argument.split('-m=')[1])
                    print('Minimum accuracy is now %f'%minimum_acc)

                if(argument.startswith('-b=')):
                    batch_size=int(argument.split('-b=')[1])
                    print('Batch size is now %d'%batch_size)

                if(argument.startswith('-e=')):
                    epochs=int(argument.split('-e=')[1])
                    print('Number of epochs is now %d'%epochs)

                if(argument.startswith('-s=')):
                    MAX_SIZE=int(argument.split('-s=')[1])
                    print('Window size is now %d'%MAX_SIZE)

                if(argument.startswith('-y=')):
                    num_of_years=int(argument.split('-y=')[1])
                    print('Going to try to gather %d years worth of data'%num_of_years)

                if(argument=='-a'):
                    USE_ADAM=True
                    print('Going to use the adam loss system over Stochastic Gradient Descent')

                if(argument=='-r'):
                    SHUFFLE_STOCKS=True
                    print('Going to shuffle the initial stock list order')

                if(argument=='-d'):

                    for ticker in tickers:
                        spy[ticker]=Robinhood().get_historical_quotes(ticker, 'day', 'year')

                    try:
                        os.unlink('tempdata.json')
                    except:
                        pass

                    json.dump(spy, open('tempdata.json', 'w'))
                    print("Download complete, you shouldn't try to download the stocks again")


                if(argument.startswith('-t=')):
                    test=int(argument.split('-t=')[1])
                    print("Going to use test %d"%test)

                    if(test==0):
                        batch_size=256
                    elif(test==1):
                        batch_size=256
                    elif(test==2):
                        epochs=50
                        batch_size=32

                if(argument.startswith('-p=')):
                    predownloaded_csv=argument.split('-p=')[1]
                    print("Going to use %s as the data source"%predownloaded_csv)
        if(predownloaded_csv==''):
            spy=json.load(open('tempdata.json'))
        else:
            import pandas as pd
            results=[]
            historicals={}
            ih=[]

            df=pd.read_csv(predownloaded_csv)

            previous_name=""

            count=0

            #for date, name, sopen, high, low, close, volume in zip(df['date'], df['Name'], df['open'], df['high'], df['low'], df['close'], df['volume']):
            for date, name, sopen, high, low, close, volume in zip(df['begins_at'], df['symbol'], df['open_price'], df['high_price'], df['low_price'], df['close_price'], df['volume']):

                if(name != previous_name and previous_name!="" and len(ih)>0):
                    historicals['historicals']=ih
                    results.append(historicals)
                    spy[name]={'results':results}
                    results=[]
                    historicals={}
                    ih=[]

                record = datetime.datetime.strptime(date, '%Y-%m-%d')
                since = datetime.datetime.now() - datetime.timedelta(days=num_of_years*365)
                ohcl={ 'volume':volume, 'open_price':sopen, 'low_price':low, 'high_price':high, 'close_price':close }

                if(record>since):
                    ih.append(ohcl)

                count=count+1

                previous_name=name

            if( previous_name!=""  and len(ih)>0):
                historicals['historicals']=ih
                results.append(historicals)
                spy[previous_name]={'results':results}

        data_dim = MAX_SIZE

        cont=True
        
        stddevfactor=1

        while(cont):
            good_stock_ticker=[]
            tmin={}
            tmax={}
            num_of_good_tickers=0
            length_in_days=len(spy['AAPL']['results'][0]['historicals'])
            timesteps=length_in_days-MAX_SIZE-1

            print("Length in days: "+str(length_in_days))


            for other_ticker in tickers:
                try:
                    if ( len(spy[other_ticker]['results'][0]['historicals'])==length_in_days ):
                        good_stock_ticker.append(other_ticker)
                        num_of_good_tickers+=1
                except:
                    pass

            nb_classes=num_of_good_tickers


            if(SHUFFLE_STOCKS):
                import random
                random.shuffle(good_stock_ticker)

            print("Number of detected valid stocks: "+str(num_of_good_tickers))


            for other_ticker in range(num_of_good_tickers):
                tmax[good_stock_ticker[other_ticker]]=max([ np.float32(spy[good_stock_ticker[other_ticker]]['results'][0]['historicals'][x]['close_price']) for x in range(length_in_days) ])
                tmin[good_stock_ticker[other_ticker]]=min([ np.float32(spy[good_stock_ticker[other_ticker]]['results'][0]['historicals'][x]['close_price']) for x in range(length_in_days) ])

            close_values=[]
            close_test_values=[]
            results=[]
            count_of_results=[]
            
            for y in range(num_of_good_tickers):
                count_of_results.append(0)

            for z in range(timesteps):
                subresult=[]
                max_value_index=-1
                max_value=-1
                for y in range(num_of_good_tickers):
                    val1=np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][MAX_SIZE+z+1]['close_price'])
                    val2=np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][MAX_SIZE+z]['close_price'])
                    tempmax=tmax[good_stock_ticker[y]]
                    tempmin=tmin[good_stock_ticker[y]]
                    if(tempmax!=tempmin):
                        current_swing=(val1-val2)/(tempmax-tempmin)
                        if(current_swing>max_value ): #and count_of_results[y]==0):
                            max_value=current_swing
                            max_value_index=y
                for y in range(num_of_good_tickers):
                    if y==max_value_index:
                        subresult.append(1)
                        count_of_results[y]+=1
                    else:
                        subresult.append(0)
                results.append(subresult)

            high_water_mark=np.mean(count_of_results)+stddevfactor*np.std(count_of_results)
            low_water_mark=np.mean(count_of_results)-stddevfactor*np.std(count_of_results)

            restart=False
            for y in range(num_of_good_tickers):
                if( not ( count_of_results[y]>=low_water_mark and count_of_results[y]<=high_water_mark ) ):
                    restart=True
                    tickers.remove(good_stock_ticker[y])
                    stddevfactor+=.25
            if(restart):
                print("\nGoing to remove any result that had more than %f entries and less than %f entries, as they are oversampled/undersampled\n"%(high_water_mark, low_water_mark))
                continue

            results=np.asarray(results)

            decoder = Sequential()

            if(test==0):

                close_values=[[[np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['close_price']) for x in range(MAX_SIZE)] for y in range(num_of_good_tickers)] for z in range(timesteps)]

                close_test_values=[[[np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['close_price']) for x in range(MAX_SIZE)] for y in range(num_of_good_tickers)] for z in range(timesteps,timesteps+1)]

                hidden=nb_classes
                decoder.add(LSTM(hidden, return_sequences=True, input_shape=( nb_classes, data_dim)))
                decoder.add(Dropout(0.5))
                decoder.add(LSTM(hidden, return_sequences=True))
                decoder.add(Dropout(0.5))
                decoder.add(LSTM(hidden))
                decoder.add(Dropout(0.5))
                decoder.add(Dense(hidden, activation='relu'))
                decoder.add(Dropout(0.5))

            elif(test==1):

                close_values=[[[np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['close_price']) for x in range(MAX_SIZE)] for y in range(num_of_good_tickers)] for z in range(timesteps)]

                close_test_values=[[[np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['close_price']) for x in range(MAX_SIZE)] for y in range(num_of_good_tickers)] for z in range(timesteps,timesteps+1)]

                hidden=24
                decoder.add(LSTM(hidden, return_sequences=True, input_shape=( nb_classes, data_dim)))
                decoder.add(Conv1D(hidden, 4, activation='relu'))
                decoder.add(LSTM(hidden, return_sequences=True))
                decoder.add(Conv1D(hidden, 3, activation='relu'))
                decoder.add(LSTM(hidden, return_sequences=True))
                decoder.add(Conv1D(hidden, 2, activation='relu'))
                decoder.add(LSTM(hidden))

                decoder.add(Dense(hidden, activation='relu'))
                decoder.add(Dropout(0.2))

            elif(test==2):

                close_values=[[[[ np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['close_price']) if chan==0 else np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['high_price']) if chan==1 else np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['low_price']) if chan==2 else np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['open_price']) if chan==3 else np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['volume']) for chan in range(5)] for x in range(MAX_SIZE)] for y in range(num_of_good_tickers)] for z in range(timesteps)]

                close_test_values=[[[[ np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['close_price']) if chan==0 else np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['high_price']) if chan==1 else np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['low_price']) if chan==2 else np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['open_price']) if chan==3 else np.float32(spy[good_stock_ticker[y]]['results'][0]['historicals'][x+z]['volume']) for chan in range(5)] for x in range(MAX_SIZE)] for y in range(num_of_good_tickers)] for z in range(timesteps,timesteps+1)]        

                hidden=20
                decoder.add(Reshape((nb_classes, MAX_SIZE, 5, 1), input_shape=(nb_classes, MAX_SIZE, 5)))
                decoder.add(ConvLSTM2D(filters=hidden, kernel_size=(6, 6), padding='same', return_sequences=True))
                decoder.add(BatchNormalization())
                decoder.add(ConvLSTM2D(filters=hidden, kernel_size=(5, 5), padding='same', return_sequences=True))
                decoder.add(BatchNormalization())
                decoder.add(ConvLSTM2D(filters=hidden, kernel_size=(4, 4), padding='same', return_sequences=True))
                decoder.add(BatchNormalization())
                decoder.add(ConvLSTM2D(filters=hidden, kernel_size=(3, 3), padding='same', return_sequences=True))
                decoder.add(BatchNormalization())
                decoder.add(Conv3D(filters=1, kernel_size=(3, 3, 3), activation='sigmoid', padding='same', data_format='channels_last'))
                decoder.add(Dense(hidden, activation='relu'))
                decoder.add(Dropout(0.2))
                decoder.add(Flatten())


            decoder.add(Dense(nb_classes, activation='softmax'))

            if(not USE_ADAM):
                sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
                decoder.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
            else:
                decoder.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

            decoder.summary()

            close_values=np.asarray(close_values)
            close_test_values=np.asarray(close_test_values)


            print("Shape of close_values is: "+str(close_values.shape))

            result=decoder.fit(close_values, results, batch_size=batch_size, epochs=epochs)
            count=epochs
            previous_acc=0
            previous_loss=0
            min_back=minimum_acc
            last_values=[]
            while(result.history['acc'][0]<minimum_acc and count<10*epochs and result.history['loss'][0]!=previous_loss):
                previous_loss=result.history['loss'][0]
                previous_acc=result.history['acc'][0]
                result=decoder.fit(close_values, results, batch_size=batch_size, epochs=1)
                count+=1
                print("Epoch: %d"%count)
                if(len(last_values)>10 and np.std(last_values[-10:])<0.0001):
                    break
                last_values.append(result.history['acc'][0])
                minimum_acc-=0.0001

            previous_acc=result.history['acc'][0]
            minimum_acc=min_back

            predictions=decoder.predict(close_test_values, batch_size=batch_size)

            if(do_main(['', good_stock_ticker[np.argmax(predictions)], '-d'])):
                print("\nSystem indicated that it should be %s with a confidence of %f and accuracy of %f\n"%(good_stock_ticker[np.argmax(predictions)], predictions[0][np.argmax(predictions)], previous_acc))

                cont=False
            else:
                print("\nSystem indicated that %s will decline tomorrow, skipping..."%good_stock_ticker[np.argmax(predictions)])
                tickers.remove(good_stock_ticker[np.argmax(predictions)])
    except:
        print("Something went wrong. Returning failure to rerun the previous test.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
