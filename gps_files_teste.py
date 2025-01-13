#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 15:59:37 2024

@author: akel
"""
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
    plt.close('all')

    gpx_file = open(filegpx, 'r')
    gpx0 = gpxpy.parse(gpx_file)

    #moving_data = gpx0.get_moving_data(raw=True)
    #print(moving_data)


    hr = []  #  batimento cardíaco
    lat = []  # latitude
    lon = []  # longitude
    ele = []  # elevação
    t = []  # datetime_instante
    n = len(gpx0.tracks[0].segments[0].points)


    date_gpx=gpx0.time
    #print(gpx0.time) #dia/hora da atividade
    for i in range(0, n, 1):
        temp= gpx0.tracks[0].segments[0].points[i]
        t.append(temp.time)
        lat.append(temp.latitude)
        lon.append(temp.longitude)
        ele.append(temp.elevation)
        hr.append(int(gpx0.tracks[0].segments[0].points[i].extensions[0][0].text))

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
        a = (lat[0 + i], lon[0 + i])
        b = (lat[1 + i], lon[1 + i])
        s.append(haversine(a, b) * 1000)  # segmentos

    d = np.cumsum(s)
    delta_ts=np.diff(ts)
    delta_d=np.diff(d)
    delta_d[0]=30
    with np.errstate(divide='ignore', invalid='ignore'):
        pace_total=(delta_ts/60.0)/(delta_d*0.001)
    #identificar pace altos.

    #limpar valores altos e baixos
    id_high=np.where(pace_total>15.0)
    temp_pace = np.delete(pace_total,id_high)
    temp_t = np.delete(delta_ts, [id_high])
    temp_d = np.delete(delta_d, [id_high])

    id_low=np.where(temp_pace< 3.0)
    pacer = np.delete(temp_pace, id_low)
    tsr= np.cumsum(np.delete(temp_t, id_low))
    dr = np.cumsum(np.delete(temp_d, id_low))
    if opt is None:
        pass
    elif (opt.lower())=='print':
        print('Total de pontos excluídos H :',len(id_high[0]))
        print('Total de pontos excluídos L :', len(id_low[0]))
        print('Tamanho vetor               :',len(pacer))
        #print('Pace médio                  :',pp_pace(np.mean(pacer)))
        #print('Pace max                    :',pp_pace(max(pacer)))
        #print('Pace min                    :',pp_pace(min(pacer)))


    return {"t" : tsr, "d" : dr, "p" : pacer,"date":date_gpx,'gpx0':gpx0}

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
NAMESPACES={'garmin_tpe': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'}
hr=A.find('garmin_tpe:hr', NAMESPACES).text
print(point[44])

print('tempo       ',point[44].time)
print('latitude    ', point[44].latitude)
print('longitude   ', point[44].longitude)
print('elevação    ', point[44].elevation)
print('hr          ', hr)




