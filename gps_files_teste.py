#!/usr/bin/env python3
"""
Created on Wed Jul 10 15:59:37 2024

@author: akel
"""
import pandas as pd
import numpy as np


def gpxfile_imp2(filegpx,**kwargs):
    """
    :param filegpx: Extract data info of gpx file from strava
    :return: time,distance e pace
    """

    import gpxpy.gpx
    from datetime import timezone, timedelta
    from haversine import haversine
    opt = kwargs.get('opt')
    if opt is None:
        pass

    gpx_file = open(filegpx, 'r')
    gpx0 = gpxpy.parse(gpx_file)


    hr = []  #  batimento cardíaco
    cad = []  #  cadencia
    lat = []  # latitude
    lon = []  # longitude
    ele = []  # elevação
    t = []  # datetime_instante
    n = len(gpx0.tracks[0].segments[0].points) # dimension data

    date_gpx=gpx0.time
    fuso = timezone(timedelta(hours=-3))
    point=gpx0.tracks[0].segments[0].points
    for i in range(0, n, 1):
        t.append(point[i].time.astimezone(fuso))
        lat.append(point[i].latitude)
        lon.append(point[i].longitude)
        ele.append(point[i].elevation)
        hr.append(int(point[i].extensions[0][0].text))
        cad.append(int(point[i].extensions[0][1].text))


    # tempo acumulado em segundos
    dt = [0]
    for i in range(0, n - 1, 1):
        dt.append((t[i + 1] - t[i]).seconds)
    ts = np.cumsum(dt)

    s = [0]
    for i in range(0, n - 1, 1):
        Pa = (lat[0 + i], lon[0 + i])
        Pb = (lat[1 + i], lon[1 + i])
        s.append(haversine(Pa, Pb) * 1000)  # segmentos

    d = np.cumsum(s)
    d_0 = d

    delta_ts=np.diff(ts)
    delta_d=np.diff(d)
    delta_d[0]=30
    with np.errstate(divide='ignore', invalid='ignore'):
        pace_total=(delta_ts/60.0)/(delta_d*0.001)
    #identificar pace altos.

    #limpar valores altos e baixos
    id_high=np.where(pace_total>3555000.0)
    temp_pace = np.delete(pace_total,id_high)
    temp_t = np.delete(delta_ts, [id_high])
    temp_d = np.delete(delta_d, [id_high])

    id_low=np.where(temp_pace< 0.0)
    pace = np.delete(temp_pace, id_low)
    tsr= np.cumsum(np.delete(temp_t, id_low))
    dr = np.cumsum(np.delete(temp_d, id_low))
    if opt is None:
        pass
    elif (opt.lower())=='print':
        print('Total de pontos excluídos H :',len(id_high[0]))
        print('Total de pontos excluídos L :', len(id_low[0]))
        print('Tamanho vetor               :',len(pace))



    dr = np.concatenate(([0], dr))
    tsr = np.concatenate(([0], tsr))
    pace= np.concatenate(([0], pace))

    dat=[t,tsr,lat,lon,dr,pace,ele,hr,cad]
    column_names = ['time','time(s)','lat','long','distance','pace','elev','hr','cad']

   # m = ['time','time(s)','lat','long','distance','pace','elev','hr','cad']
    df = pd.DataFrame(dat).T
    df.columns = [column_names]
    #print(dr[0],dr[1],dr[12])
    #df.rename(index={0:"lat", 1: "lon"})
    #print(df)

    return {"t" : tsr, "d" : dr, "p" : pace,"date":date_gpx,'gpx0':gpx0,'df':df}

import matplotlib.pyplot as plt
import numpy as np

file ='343_366_Meia_maratona_OAB.gpx'
#file='12_365_longo_.gpx'
out=gpxfile_imp2(file)
df=out['df']
gpx=out['gpx0']
print('')

pd.set_option('display.max_columns',9)
pd.set_option('display.width', 10000)
print(df)
keys=df.keys()
print(df['time(s)'])
print(df['elev'])
print(out['t'][0])
elev=df['elev']
a=np.ediff1d(elev)
a= np.concatenate(([0], a))

print(a)
gh=0
for n in range(len(a)):
    if a[n]>=0:
        gh+=a[n]
print(gh)
fig, ax = plt.subplots()
ax.set_aspect(aspect=250)
ax.plot(df['distance'],elev)
plt.show()





