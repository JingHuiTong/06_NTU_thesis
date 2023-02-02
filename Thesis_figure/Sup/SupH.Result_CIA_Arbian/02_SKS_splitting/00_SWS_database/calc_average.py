import glob,os 
import numpy as np
import pandas as pd
csvfile = '../Kaviani_etal_Zargos_2021.csv'
df = pd.read_csv(csvfile)

def angle_mean(dt, phi, ddt, dphi):
    dt=np.array(dt, dtype='float64')
    phi=np.array(phi, dtype='float64')
    ddt=np.array(ddt, dtype='float64')
    dphi=np.array(dphi, dtype='float64')
    x = dt*np.cos(2*phi*np.pi/180.0)
    y = dt*np.sin(2*phi*np.pi/180.0)
    c = x + 1j*y
    m = np.mean(c)

    phase = np.angle(m, deg=True)/2.
    radius = np.abs(m)
    dphase = np.sqrt(np.sum(dphi**2))/len(x)
    dradius = np.sqrt(np.sum(ddt**2))/len(x)

    return phase, dphase, radius, dradius
    
    
STATION = set(df['Station'])
newdf = {'sta':[],
        'stlat':[],
        'stlon':[],
        'phi':[],
        'dphi':[],
        'dt':[],
        'ddt':[],
        'num':[]}
for sta in STATION:
    print(sta)
    dff = df[df['Station']==sta][df['Phi']!='Null']
    num = len(dff)
    if num != 0:
        stlat = dff['Sta_Lat'].values[0]
        stlon = dff['Sta_Lon'].values[0]
    
        dt_ori = dff['dt'].to_list()
        phi_ori = dff['Phi'].to_list()
        ddt_ori = dff['std_dt'].to_list()
        dphi_ori = dff['std_phi'].to_list()
        phi, dphi, dt, ddt = angle_mean(dt_ori,phi_ori,ddt_ori,dphi_ori )
    
        newdf['sta'].append(sta)
        newdf['stlat'].append(stlat)
        newdf['stlon'].append(stlon)
        newdf['phi'].append(phi)
        newdf['dphi'].append(dphi)
        newdf['dt'].append(dt)
        newdf['ddt'].append(ddt)
        newdf['num'].append(num)
    
newdf = pd.DataFrame(newdf)
newdf.to_csv('Kaviani2021_average.csv',index=False)
    # print(sta, phi, dphi, dt, ddt)
    
    
    
    
    
    
    