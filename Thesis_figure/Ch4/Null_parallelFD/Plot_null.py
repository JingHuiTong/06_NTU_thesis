#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os,glob
import pandas as pd
import pygmt
import pickle
import warnings  
import numpy as np
warnings.filterwarnings("ignore")


# In[2]:



STApath = '/Volumes/home/Research/DataBase/01_Armenia/Station_info_2.csv'
dS = pd.read_csv(STApath)
path    = '/Volumes/home/Research/STEP/02_Station_result_csv'
bazcsv = 'baz.csv'
dB = pd.read_csv(bazcsv)


reference = 46.8
std = 16.8


# In[9]:


def PygmtBegin(figmap, region, title):
    figmap.basemap(region=region, projection="M15c", frame = ['x1f0.5', 'y1f0.5', f'nSeW+t"{title}"'])
    figmap.grdimage('@earth_relief_15s',region =region, cmap="/Volumes/home/Research/Python/eleva.cpt",monochrome=True, shading=True, transparency=60)
    figmap.coast(resolution = 'h', shorelines ='1/thinnest,black', water='white', borders = '1/0.25p')
#     figmap.plot(data=smooth_fault,pen='1p,brown')
    Volcano = '/Volumes/home/Research/DataBase/01_Armenia/02_Volcano_list.csv'
    dv = pd.read_csv(Volcano)
    dv_ = dv[dv['Plottype']==1]
    figmap.plot(x=dv_['lon'],y=dv_['lat'],style="kvolcano/0.4c", pen='0.1p,black', color="black")
    dv__ = dv[dv['Plottype']==3]
    figmap.plot(x=dv__['lon'],y=dv__['lat'],style="kvolcano/0.4c", pen='0.1p,', color="120")    


# In[5]:


da = pd.read_csv('/Volumes/home/Research/STEP/05_Station_result_statistics/Station_SK(K)S_2010-2020average_v7.csv')

Nodatasta=[]
NULLsta=[]
for a in range(len(da)):
    nonNull = da['nonNull'].values[a]
    Null = da['Null'].values[a]
    Station = str(da['Station'].values[a]).rsplit('.')[-1]
    
    if nonNull == 0 and Null<=3:
        Nodatasta.append(Station)
    elif nonNull == 0 and Null>3:
        NULLsta.append(Station)
        


# In[25]:


#=================Lesser
# STAlist = ['KIV','ONI','URAV','AMBR','TKBL','GUDA','GUDG','DDFL','LGD','CHVG','KHVA','ZKT']
#
# region = [41.5,47,41,44.5]
# filename = f'Null_result_GC'

#=================Lesser
# STAlist = ['BATM','BCA','ABST','BKRG','BURN','BRNG','AZMN','AKH','GANZ','BGD','KANZ','SEAG','DMNI','KZRT','TBLG','DGRG','TRLT','TRLG']
#
# region = [40.5,45.7,40.7,42.3]
# filename = f'Null_result_LC'

#=================AM
STAlist = ['BAUR','ARZA','TSAP','LICH','ALAV','ZARN','NAVR',
           'BYUR','GERK','KECH','VAND','MAGY','SHEN','GANJ',
           'QZX','TASB','GNI']

region = [43,46.7,39.5,41.5]
filename = f'Null_result_AM'


# In[26]:


method = 'SC'
figmap = pygmt.Figure()
region = region
title  = f'Individual {method}'
PygmtBegin(figmap,region,title)


for i in range(len(dS)):
    sta = dS['station'].values[i]
    if sta in STAlist: 
        stlat = dS['lat'].values[i]
        stlon = dS['lon'].values[i]
        for resultpath in sorted(glob.glob(f'{path}/2010-2020_*_classify_220913/*{sta}*result_v2.csv')):
            df = pd.read_csv(resultpath)
            dff = df[df['Null']==True][df['Pick']==True]
            
            for i in range(len(dff)):
                event = dff['Event'].values[i]
                evlat = dff['Ev_lat'].values[i]
                evlon = dff['Ev_lon'].values[i]
                evdep = dff['Depth'].values[i]
                
                baz = dB['baz'][dB['station']==sta][dB['event']==event].values[0]
                data = [[stlon, stlat, baz-90, 2, 0.7*40]]
                figmap.plot(data=data, style="J", color='black', pen="0.5p,white",transparency=35, no_clip=True)        

        if sta in NULLsta:
            figmap.plot(x=stlon, y=stlat, style="c0.25c", color='white', pen="0.5p,40")
        elif sta in Nodatasta:
            figmap.plot(x=stlon, y=stlat, style="c0.2c", color='180', pen="0.5p,40")
        else:
            figmap.plot(x=stlon, y=stlat, style="c0.2c", color='black', pen="0.5p,white")
        if sta == 'GUDG' or sta == 'TRLG' or sta == 'SEAG':
            figmap.text(x=stlon,y=stlat-0.2,text=sta, font="8p,Times-Bold,black",fill='white',transparency=30)
        else:
            figmap.text(x=stlon,y=stlat-0.1,text=sta, font="8p,Times-Bold,black",fill='white',transparency=30)
figmap.show()
figmap.savefig(f'{filename}_v4.png',dpi=200)
figmap.savefig(f'{filename}_v4.pdf',dpi=200)




