import pandas as pd
import glob, os

path = '/Users/tong/Documents/99_temp/Research/STEP/14_result_removeD-220913'


GOOD = 0
FAIR = 0 
POOR = 0
NULL = 0
for csvpath in glob.glob(f'{path}/*classify/*v2.csv'):
    df = pd.read_csv(csvpath)
    df = df[df['Pick']==True]
    
    NULL += len(df[df['Null']==True])
    GOOD += len(df[df['Null']==False][df['Quality']=='Good'])
    FAIR += len(df[df['Null']==False][df['Quality']=='Fair'])
    POOR += len(df[df['Null']==False][df['Quality']=='Poor'])
    
    
print(f'Good : {GOOD}')
print(f'Fair : {FAIR}')
print(f'Poor : {POOR}')
print(f'Null : {NULL}')