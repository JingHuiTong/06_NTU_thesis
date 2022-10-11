#!/usr/bin/env python
# coding: utf-8


import os,glob
import pandas as pd
import pygmt
import pickle
import warnings  
import numpy as np

warnings.filterwarnings("ignore")


STApath = '/Users/tong/Documents/99_temp/Research/DataBase/01_Armenia/Station_info_2.csv'
dS = pd.read_csv(STApath)
path    = '/Users/tong/Documents/99_temp/Research/STEP/14_result_removeD-220913'
figpath = '/Volumes/home/Research/STEP/12_PiercePoint'

method = 'SC'


def angle_mean(dt, phi, ddt, dphi):
    dt=np.array(dt)
    phi=np.array(phi)
    ddt=np.array(ddt)
    dphi=np.array(dphi)
    x = dt*np.cos(2*phi*np.pi/180.0)
    y = dt*np.sin(2*phi*np.pi/180.0)
    c = x + 1j*y
    m = np.mean(c)

    phase = np.angle(m, deg=True)/2.
    radius = np.abs(m)
    dphase = np.sqrt(np.sum(dphi**2))/len(x)
    dradius = np.sqrt(np.sum(ddt**2))/len(x)
    print(phase, dphase, radius, dradius)
    return phase, dphase, radius, dradius


# ## Histogram 

# In[5]:


SC = {'neg_philist' : [],
      'neg_dtlist' : [],
      'neg2_philist' : [],
      'pos_philist' : [],
      'pos_dtlist' : [] }
RC = {'neg_philist' : [],
      'neg_dtlist' : [],
      'neg2_philist' : [],
      'pos_philist' : [],
      'pos_dtlist' : [] }
for ss in range(len(dS)):
    NET = dS['network'].values[ss]
    STA = dS['station'].values[ss]
    st_lat = dS['lat'].values[ss]
    st_lon = dS['lon'].values[ss]
    NetSta = f'{NET}.{STA}'
    print(NetSta)
    if STA == 'CMCY' or STA == 'DGRL' or NET =='BI':
        pass
    else:
        for resultpath in sorted(glob.glob(f'{path}/2010-2020_*_classify/{NET}.{STA}*result_v2.csv')):
            print(resultpath)
            df = pd.read_csv(resultpath)
            dff = df[df['Null']==False][df['Quality']!='Poor'][df['Pick']==True]
            for i in range(len(dff)):
                event = dff['Event'].values[i]
                evlat = dff['Ev_lat'].values[i]
                evlon = dff['Ev_lon'].values[i]
                evdep = dff['Depth'].values[i]
                phase = dff['Phase'].values[i]

                phi = dff['SCPhi'].values[i]
                dt  = dff['SCdt'].values[i]
                if phi > 0: 
                    SC['pos_philist'].append(phi)
                    SC['pos_dtlist'].append(dt) 
                else: 
                    SC['neg2_philist'].append((phi+180))
                    SC['neg_philist'].append(phi)
                    SC['neg_dtlist'].append(dt) 

                phi = dff['RCPhi'].values[i]
                dt  = dff['RCdt'].values[i]

                if phi > 0: 
                    RC['pos_philist'].append(phi)
                    RC['pos_dtlist'].append(dt) 
                else: 
                    RC['neg2_philist'].append((phi+180))
                    RC['neg_philist'].append(phi)
                    RC['neg_dtlist'].append(dt) 


# In[6]:


# from scipy.stats import circmean, circstd
# def mean(phi, dt):
#     newphi = []
#     for i in phi:
#         newphi.append(i*np.pi/180)
#     phimean = circmean(newphi)*180/np.pi
#     phistd  = circstd(newphi)*180/np.pi
#     dtmean  = np.mean(dt)
#     dtstd  = np.std(dt)
#     print(phimean,phistd,dtmean,dtstd)
#     return phimean,phistd,dtmean,dtstd
# phimean,phistd,dtmean,dtstd = mean(SC['pos_philist'], SC['pos_dtlist'])
# phimean,phistd,dtmean,dtstd = mean(SC['neg2_philist'], SC['neg_dtlist'])
#
# phimean,phistd,dtmean,dtstd = mean(RC['pos_philist'], RC['pos_dtlist'])
# phimean,phistd,dtmean,dtstd = mean(RC['neg2_philist'], RC['neg_dtlist'])
#



# In[46]:

#
# SCphase, SCdphase, SCradius, SCdradius = angle_mean(SC['pos_dtlist'], SC['pos_philist'], SC['pos_ddtlist'], SC['pos_dphilist'] )
# SCphase_, SCdphase_, SCradius_, SCdradius_ = angle_mean(SC['neg_dtlist'], SC['neg2_philist'], SC['neg_ddtlist'], SC['neg_dphilist'])
# RCphase, RCdphase, RCradius, RCdradius = angle_mean(RC['pos_dtlist'], RC['pos_philist'], RC['pos_ddtlist'], RC['pos_dphilist'] )
# RCphase_, RCdphase_, RCradius_, RCdradius_ = angle_mean(RC['neg_dtlist'], RC['neg2_philist'], RC['neg_ddtlist'], RC['neg_dphilist'])
#

# In[98]:





# In[8]:


fig = pygmt.Figure()
# -Gp解析度/種類代碼:B背景色F前景色
with fig.subplot(nrows=2, ncols=1, figsize=("12c", "10c"), frame=["af", "WS"],
    margins=["0.1c", "0.5c"], title="Individual spliiting results",):
    fig.basemap(region=[-90, 90, 0, 70], projection="X?", frame=["xa10f10", "ya10f5", "WS"], panel=[0])

    fig.histogram(
        data=RC['pos_philist'],
        frame=[ 'x+l"Fast Direction (\\260)"', 'y+l"Counts"'],
        series=10, fill="p400/12:BblackFwhite", pen="0.8p", histtype=0, label='RC')
    fig.histogram(
        data=SC['pos_philist'],
        series=10, fill='red@60', histtype=0,label='SC')
    fig.histogram(
        data=RC['neg_philist'],
        series=10, fill="P400/12:BblackFwhite", pen="0.8p", histtype=0)  
    fig.histogram(
        data=SC['neg_philist'],
        series=10, fill='red@50', histtype=0)
    fig.legend(position='JTL+jTL+o0.2c')
    fig.text(x=-90,y=85,text=f'SC = Pos: 45.97\\260+15.60 1.17+0.45s, Neg: -51.64\\260+19.48 1.17+0.80s',justify='LT',no_clip=True)
    fig.text(x=-90,y=80,text='RC = Pos: 45.85\\260+12.27 1.05+0.39s, Neg: -51.22\\260+15.76 1.06+0.82s',justify='LT',no_clip=True)
    fig.basemap(region=[0, 4, 0, 60], projection="X?", frame=['xa1f0.2','ya10f5', "WS"], panel=[1, 0])
    fig.histogram(
        data=RC['pos_dtlist']+RC['neg_dtlist'],
        series=0.2, fill="p400/12:BblackFwhite", pen="0.8p", histtype=0)
    fig.histogram(
        data=SC['pos_dtlist']+SC['neg_dtlist'],
        frame=[ 'x+l"Delay time (s)"', 'y+l"Counts"'],
        series=0.2, fill='red@60', histtype=0)


fig.show()
fig.savefig('Histogram_2method_v3.png',dpi=300)
fig.savefig('Histogram_2method_v3.pdf',dpi=300)


# In[ ]:




