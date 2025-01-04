#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 15:59:37 2024

@author: akel
"""

#import gpxpy

import numpy as np


import gpxpy.gpx
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta
from haversine import haversine

plt.close('all')

# gpx_file = open('Morning_Run1.gpx', 'r')
gpx_file = open('173_365_16_km.gpx', 'r')
gpx_file = open('26122024.gpx', 'r')

gpx0 = gpxpy.parse(gpx_file)


hr = []  # batimento cardiaco
lat = []  # latitude
lon = []  # longitude
ele = []  # elevação
t = []  # datetime_instante
n = len(gpx0.tracks[0].segments[0].points)  # dimensao do vetor

for i in range(0, n, 1):
    temp = gpx0.tracks[0].segments[0].points[i]
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

# calculo da distancia( haversine formule)
# 2R × sen-¹(√[sen²((θ₂ - θ₁)/2) + cosθ₁ × cosθ₂ ...
# × sen²((φ₂ - φ₁)/2)])
s = [0]
for i in range(0, n - 1, 1):
    A = (lat[0 + i], lon[0 + i])
    B = (lat[1 + i], lon[1 + i])
    s.append(haversine(A, B) * 1000)  # segmentos

d = np.cumsum(s)  # distancia percorrida

df = np.diff(ele)
df = np.append(df, 0)

# calculo pace
print(len(ts))
print(len(d))



# v1=[]
# for i in range(0,int(max(d)/1000)+1):
#     ind=np.where((d>=i*1000)&(d<=(i+1)*1000))
#     v1.append(np.sum[np.array(s[ind])])
#     print(v1)
print('cansei de fazer')


# p=((np.array(v)*3.6)**(-1))*60
# plt.plot(np.cumsum(d5),v)
# print(np.mean(p))

# fig, ax = plt.subplots(figsize=(19.20,10.80))
# fig.canvas.set_window_title('Heart rate')
# ax.plot(th,hr,'r',label='HR')
# formatter = DateFormatter('%H:%M:%S',fuso)
# ax.xaxis.set_major_formatter(formatter)
# plt.legend()
# ax.set_ylabel('Heart rate')
# plt.grid(True)


# fig2, ax = plt.subplots(figsize=(19.20,10.80))
# fig2.canvas.set_window_title('elevacao')

# ax.plot(d,ele,'*k',label='elevacao')
# plt.legend()
# ax.set_ylabel('elevacao')
# plt.grid(True)


# plt.plot(d,df)

# pos_count, neg_count = 0, 0
# for i in df:
#     print('dff=',i)


#     if i >= 0:
#         pos_count += i
#         print('soma=',pos_count)
#         time.sleep(1)

#     else:
#         neg_count += i

# print("Positive numbers in the list: ", pos_count)
# print("Negative numbers in the list: ", neg_count)


# fig, ax = plt.subplots(figsize=(19.20,10.80))

# fig.canvas.set_window_title('Leitura gpstrack')
# ax.plot(t,hr,'r',label='heart rate')
# ax.gca().set_title("1 - tzinfo NO, xaxis_date = NO, formatter=NO")

# #ax.plot(dates_sim,sim - dRMSE,'r--')
# #ax.plot(dates_sim,sim + dRMSE,'r--')
# #ax.fill_between(dates_sim, sim - dRMSE, sim + dRMSE, alpha=0.2)
# #ax.xaxis.set_major_formatter(formatter)
# #plt.ylim(0,1100)
# #plt.xlim(pd.Timestamp('2020-03-15'),pd.Timestamp('2020-06-15'))
# plt.grid('major')
# ax.set_ylabel('Heart rate')
# plt.legend()


# plt.plot(t,ele)

