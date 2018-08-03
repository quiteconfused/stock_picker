#!/usr/bin/python

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import os,sys

import subprocess

df = pd.read_csv(sys.argv[1])

STDDEVDIFF=1.5

countnames={}

for chance,acc,conf,loss,name in zip(df['chance_to_win'],df['accuracy'],df['confidence'],df['loss'],df['ticker']):
    if name not in countnames:
        countnames[name]=1
    else:
        countnames[name]+=1

numofnames=[]
for name in df['ticker']:
    numofnames.append(countnames[name])

for chance,acc,conf,loss,name in zip(df['chance_to_win'],df['accuracy'],df['confidence'],df['loss'],df['ticker']):
    if (acc>=np.mean(df['accuracy'])-STDDEVDIFF*np.std(df['accuracy']) and acc<=np.mean(df['accuracy'])+STDDEVDIFF*np.std(df['accuracy']) and
        conf>=np.mean(df['confidence'])-STDDEVDIFF*np.std(df['confidence']) and conf<=np.mean(df['confidence'])+STDDEVDIFF*np.std(df['confidence']) and
        chance>=np.mean(df['chance_to_win'])-STDDEVDIFF*np.std(df['chance_to_win']) and chance<=np.mean(df['chance_to_win'])+STDDEVDIFF*np.std(df['chance_to_win']) and
        countnames[name]>=np.mean(numofnames)-STDDEVDIFF*np.std(numofnames) and countnames[name]<=np.mean(numofnames)+STDDEVDIFF*np.std(numofnames) and
        loss>=np.mean(df['loss'])-STDDEVDIFF*np.std(df['loss']) and loss<=np.mean(df['loss'])+STDDEVDIFF*np.std(df['loss'])):
        print(str(chance)+' '+str(acc)+' '+str(conf)+' '+str(loss)+' '+str(name))



