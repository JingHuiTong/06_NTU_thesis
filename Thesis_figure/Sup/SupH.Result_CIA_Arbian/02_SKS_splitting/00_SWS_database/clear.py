import pandas as pd 

df = pd.read_csv('splittingDB.txt',sep='|')

id = 181

dff = df[df['refID']==id]


newdf = {'station':[],
    'lon':[],
    'lat':[],
    'phi':[],
    'dt':[]}
for i in range(len(dff)):
    station = dff['Station'].values[i]
    stlat = dff['Latitude'].values[i]
    stlon = dff['Longitude'].values[i]
    phi = dff['phi'].values[i]
    dt = dff['dt'].values[i]
    newdf['station'].append(station)
    newdf['lon'].append(stlon)
    newdf['lat'].append(stlat)
    newdf['phi'].append(phi)
    newdf['dt'].append(dt)
    
newdf = pd.DataFrame(newdf)
newdf.to_csv('Hansen2006.csv',index=False)
    