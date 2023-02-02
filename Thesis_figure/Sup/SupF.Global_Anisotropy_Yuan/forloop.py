import glob,os

path = 'Modelxy_2x2'
qqq = [100,150,200,250,300]

for xyfile in sorted(glob.glob(f'{path}/0???km_2x2.xy')):

    file=xyfile.rsplit('/')[-1]
    depth=int(file.rsplit('km')[0])
    
    if depth in qqq:
        cmd = '''
        csh Global_anisotropy.gmt %(file)s %(depth)i
        ''' %locals()
        os.system(cmd)
        print(f'============finish {depth}')    