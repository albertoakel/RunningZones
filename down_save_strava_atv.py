# id_cliente:146082
# client_secret: e3a7c42125c7e3ba3b755735fb08bce9d2713abd
# token: c533b4fa839707c05da146c6669ee8ed83d4996c
# refreshtoken: 67a24bf77addf8ec6c36112a0f37f4348f23b4e4

import requests
import datetime
import locale
from datetime import timedelta
import numpy as np

import urllib3
import pandas as pd

locale.setlocale(locale.LC_TIME, "pt_BR.utf8")  # Define o idioma


def call_strava():
    urllib3.disable_warnings()
    auth_url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': "146082",
        'client_secret': 'e3a7c42125c7e3ba3b755735fb08bce9d2713abd',
        'refresh_token': '4e6bbf53f4023f48fb9b433a10aa8502f16768c0',
        'grant_type': "refresh_token",
        'f': 'json'}
    # solicitação de token e sua atualização
    print('solicitação de token..\n')
    response = requests.post(auth_url, data=payload, verify=False)
    acess_tkn = response.json()["access_token"]
    rfres_tkn = response.json()["refresh_token"]
    countd = response.json()["expires_in"]

    print('acess token:', acess_tkn)
    print('refresh :', rfres_tkn)
    print('countdown:','0' + str(int(countd / 3600)) +
          ':' + str(int(((countd / 3600) - int(countd / 3600)) * 60)) +
          ':' + str(int((((countd / 3600) - int(countd / 3600)) * 60 - int(((countd / 3600) - int(countd / 3600)) * 60)) * 60)))

    # solicita dados gerais das atividades do atleta (usando o acesse token atualizado).
    # No headers é adicionado o token de acesso o qual é atualizado a cada 6h.
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + acess_tkn}

    pagina=9
    act=100
    param = {'per_page': act, 'page': pagina}  # até 200 por página.
    response1 = requests.get(activites_url, headers=header, params=param).json()
    data200= {}  #dataframedearmazenadomento
    for i in range(act):
        activity_id = response1[i]['id']
        sport=response1[i]['sport_type']
        st_date = datetime.datetime.strptime(response1[i]['start_date_local'], "%Y-%m-%dT%H:%M:%SZ")

    # '''
    #     dataset contém diversas informações das atividades. Maiores detalhes
    #     aqui: https://developers.strava.com/docs/reference/#api-models-DetailedActivity
    #     para detalhamento de uma atividade, precisamos obter o ID desta e realizar uma nova
    #     request.
    #  '''
        if sport == 'Run':
            #print('chamar função corrida')
            out=call_run(header,activity_id,st_date)
            label_df=st_date.strftime('%d/%m/%Y-%H:%M')
            data200[label_df] = out  # Armazena com uma chave nomeada
            df_geral = pd.concat([df.assign(date=name) for name, df in data200.items()], ignore_index=True)
            print(i,st_date.strftime('%H:%M %d/%m/%Y'), out.shape)

    return df_geral

def call_run(header ,activity_id,st_date):

    '''
    # https: // developers.strava.com / docs / reference /  # api-models-StreamSet
    '''

    detail_act_url = 'https://www.strava.com/api/v3/activities/' + str(activity_id) + '/streams'
    params = {'keys': 'time,distance,latlng,altitude,velocity_smooth,heartrate,cadence,moving,'
                      'grade_smooth','key_by_type': 'true'}

    response2 = requests.get(detail_act_url, headers=header, params=params)
    streams = response2.json()

    time = streams['time']['data']
    distance = streams['distance']['data']
    altitude = streams['altitude']['data']
    heartrate = streams['heartrate']['data']
    velocity = streams['velocity_smooth']['data']
    cadence = streams['cadence']['data']
    moving = streams['moving']['data']

    # condição corrida em esteira
    if len(streams) == 9:
        latlng = streams['latlng']['data']
    else:
        latlng = [np.nan] * len(time)

    pace = []
    for j in range(len(velocity)):
        if velocity[j] < 0.75:
            pace.append(0)
        else:
            pace.append(1000 / (60 * velocity[j]))

    hour = []

    for i in range(len(time)):
        time_add = timedelta(hours=0, minutes=0, seconds=time[i])
        hour.append(st_date + time_add)

    # create dataframe
    res = zip(hour, time, distance, latlng, altitude, heartrate, velocity, pace, moving, cadence)
    res = list(res)

    df = pd.DataFrame(res, columns=['hour', 'time',
                                         'distance', 'latlng',
                                         'altitude', 'heartrate',
                                         'velocity(m/s)', 'pace',
                                         'moving', 'cadence'])
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_row', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)
    #print(st_date.strftime('%H:%M %d/%m/%Y'),df.shape)
    return df



DF=call_strava()

pd.set_option('display.max_row', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

DF['week'] = (pd.to_datetime(DF['date'], format='%d/%m/%Y-%H:%M')).dt.isocalendar().week
print(DF.shape)
N=len(DF)
#print(DF)

# filename='file_strava.'+DF['date'][0][0:10]+'-'+DF['date'][N-1][0:10]+'.parquet'
# filename = filename.replace("/", "-")
# print(filename)
# DF.to_parquet(filename, index=False)  # Salvar


