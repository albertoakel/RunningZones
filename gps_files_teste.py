#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 15:59:37 2024

@author: akel
"""
import pandas as pd
import numpy as np
from numpy.ma.core import append


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

    COLUMN_NAMES = ['latitude', 'longitude', 'elevation','time']

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

    # calculo do tempo com fuso horario
    fuso = timezone(timedelta(hours=-3))
    th = []
    for i in range(0, n, 1):
        th.append(t[i].astimezone(fuso))

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
        #print('Pace médio                  :',pp_pace(np.mean(pacer)))
        #print('Pace max                    :',pp_pace(max(pacer)))
        #print('Pace min                    :',pp_pace(min(pacer)))

    dr = np.concatenate(([0], dr))
    tsr = np.concatenate(([0], tsr))
    pace= np.concatenate(([0], pace))

    dat=[t,tsr,lat,lon,dr,pace,ele,hr,cad]
    m = ['time','cum time(s)','lat','long','distance','pace','elev','hr','cad']
    df = pd.DataFrame(dat).T
    df.columns = [m]
    print(dr[0],dr[1],dr[12])
    #df.rename(index={0:"lat", 1: "lon"})
    print(df)

    return {"t" : tsr, "d" : dr, "p" : pace,"date":date_gpx,'gpx0':gpx0}

import numpy as np


#import gpxpy.gpx
import matplotlib.pyplot as plt
from datetime import timezone, timedelta
from haversine import haversine



file ='343_366_Meia_maratona_OAB.gpx'

out=gpxfile_imp2(file)
gpx=out['gpx0']
print('')
track=gpx.tracks[0]
segment=track.segments[0]
point=segment.points
print(len(segment.points))
A=point[44].extensions[0]
hr= int(point[44].extensions[0][0].text)
cad=int(point[44].extensions[0][1].text)
# NAMESPACES={'garmin_tpe': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'}
# hr=A.find('garmin_tpe:hr', NAMESPACES).text
# cad=A.find('garmin_tpe:cad', NAMESPACES).text

# print(point[44])
#
# print('tempo       ',point[44].time)
# print('latitude    ', point[44].latitude)
# print('longitude   ', point[44].longitude)
# print('elevação    ', point[44].elevation)
print('dist d2 ',segment.length_2d())
print('dist d2 ',segment.length_3d())
print('distancia',out['d'][-1])


m=['lat','long','C','D']
lat=['1a','2a','3a','4a']
long=['1b','2b','3b','4b']
cc=['1c','2c','3c','4c']
dd=['1d','2d','3d','4d']
dat=[lat,long]
#print('2--->',type(dat),np.shape(dat))

#df=pd.DataFrame(dat,columns=m)
#print(df)






