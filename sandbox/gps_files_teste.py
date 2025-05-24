#!/usr/bin/env python3
"""
Created on Wed Jul 10 15:59:37 2024

@author: akel
"""
import pandas as pd
from parse_fit import *
import numpy as np
from numpy.random import laplace


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
    delta_d=[]
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
    delta_d[0]=0
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


    dr = np.concatenate(([0], dr))    #add zero first row
    tsr = np.concatenate(([0], tsr))  #
    pace= np.concatenate(([0], pace)) #

    dat=[t,tsr,lat,lon,dr,pace,ele,hr,cad]
    column_names = ['time','time(s)','lat','long','distance','pace','elev','hr','cad']

    df = pd.DataFrame(dat).T
    df.columns = [column_names]
    df = df.drop(len(df) - 1) #remove last row dataframe

    #print(dr[0],dr[1],dr[12])
    #df.rename(index={0:"lat", 1: "lon"})
    #print(df)
    return {"t": tsr, "d": dr, "p": pace, "date": date_gpx, 'gpx0': gpx0, 'df': df}



def gpxfitfile_imp(file_fit):
    import fitdecode

    print('fit file')


            # This frame contains data about a "track point".


    return

import matplotlib.pyplot as plt

#file='18_365.gpx'
file ='343_366_Meia_maratona_OAB.gpx'
#file='activity_17992136354.gpx'
#file_fit='05_366_corrida_leve.fit'
out=gpxfile_imp2(file)
df=out['df']
print(df)
t2=df['time(s)'].to_numpy(dtype='float32')
#t2=np.transpose(t2)
t0=out['t']


#print(t2,t0)
#print(t2[5]+t0[5])
# laps_df, points_df = get_dataframes(file_fit)
# #print('LAPS:')
# print(laps_df)
# print(laps_df.keys())
# print(points_df.keys())
# print(laps_df['total_distance'],laps_df['total_elapsed_time']/60)
# print(points_df['speed'])
# #print('\nPOINTS:')
#print(points_df)
#out=gpxfitfile_imp(file_fit)

#A=fitdecode.FitReader(file_fit)
#print(out['t'])
# for i in range(len(t0)):
#     print(t0[i],t2[i])



print('tempo=',t0[5])
print(t2[5]+t0[5])
#print(df.iloc[-1])