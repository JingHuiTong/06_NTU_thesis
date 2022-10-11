import os,glob
import pandas as pd
import pickle
import warnings  
import numpy as np
from obspy.geodetics.base import gps2dist_azimuth
warnings.filterwarnings("ignore")


# In[2]:



STApath = '/Users/tong/Documents/99_temp/Research/DataBase/01_Armenia/Station_info_2.csv'
dS = pd.read_csv(STApath)
path    = '/Users/tong/Documents/99_temp/Research/STEP/14_result_removeD-220913'

newdf = {'station':[],
         'event':[],
         'baz':[]}

for i in range(len(dS)):
    sta = dS['station'].values[i]

    stlat = dS['lat'].values[i]
    stlon = dS['lon'].values[i]
    for resultpath in sorted(glob.glob(f'{path}/2010-2020_*_classify/*{sta}*result_v2.csv')):
        df = pd.read_csv(resultpath)
        dff = df[df['Null']==True][df['Pick']==True]
        
        for i in range(len(dff)):
            event = dff['Event'].values[i]
            evlat = dff['Ev_lat'].values[i]
            evlon = dff['Ev_lon'].values[i]
            evdep = dff['Depth'].values[i]
            dist, az , baz = gps2dist_azimuth(evlat,evlon,stlat,stlon)
            
            newdf['station'].append(sta)
            newdf['event'].append(event)
            newdf['baz'].append(baz)

newdf = pd.DataFrame(newdf)
newdf.to_csv('baz.csv',index=False)