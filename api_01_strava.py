# id_cliente:146082
# client_secret: e3a7c42125c7e3ba3b755735fb08bce9d2713abd
# token: c533b4fa839707c05da146c6669ee8ed83d4996c
# refreshtoken: 67a24bf77addf8ec6c36112a0f37f4348f23b4e4

import requests
import datetime
from datetime import timedelta
import urllib3
import pandas as pd


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
    print('countdown:',
          '0' + str(int(countd / 3600)) + ':' + str(int(((countd / 3600) - int(countd / 3600)) * 60)) + ':' + str(int(((
                                                                                                                                   (
                                                                                                                                               countd / 3600) - int(
                                                                                                                               countd / 3600)) * 60 - int(
              ((countd / 3600) - int(countd / 3600)) * 60)) * 60)))

    # solicita dados gerais das atividades do atleta (usando o acesse token atualizado).
    # No headers é adicionado o token de acesso o qual é atualizado a cada 6h.
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + acess_tkn}
    param = {'per_page': 200, 'page': 1}  # 200 por página.
    response1 = requests.get(activites_url, headers=header, params=param).json()
    activity_id = response1[0]['id']
    mv_time = response1[0]['moving_time']
    elapsed_time = response1[0]['elapsed_time']
    tipo_atv = response1[0]['type']
    print('--------')

    # converte o str em datetime
    st_date = datetime.datetime.strptime(response1[0]['start_date_local'], "%Y-%m-%dT%H:%M:%SZ")
    # print(st_date.strftime('%H:%M %d/%m/%Y'))

    '''
    dataset contém diversas informações das atividades. Maiores detalhes
    aqui: https://developers.strava.com/docs/reference/#api-models-DetailedActivity
    para detalhamento de uma atividade, precisamos obter o ID desta e realizar uma nova
    request.
    '''
    detail_act_url = 'https://www.strava.com/api/v3/activities/' + str(activity_id) + '/streams'

    # os parâmetros para o novo resquest podem ser consultados aqui:
    # https://developers.strava.com/docs/reference/#api-models-StreamSet

    params = {'keys': 'time,distance,latlng,altitude,velocity_smooth,heartrate,cadence,moving,grade_smooth',
              'key_by_type': 'true'}
    response2 = requests.get(detail_act_url, headers=header, params=params)
    streams = response2.json()

    # pd.set_option('display.max_columns',None)
    # pd.set_option('display.max_row',None)
    # pd.set_option('display.max_colwidth',None)
    # pd.set_option('display.width',None)

    time = streams['time']['data']
    distance = streams['distance']['data']
    latlng = streams['latlng']['data']
    altitude = streams['altitude']['data']
    heartrate = streams['heartrate']['data']
    velocity = streams['velocity_smooth']['data']
    cadence = streams['cadence']['data']
    moving = streams['moving']['data']
    #
    pace = [0.6 ** (-1) * x for x in velocity]
    hour = []
    for i in range(len(time)):
        time_add = timedelta(hours=0, minutes=0, seconds=time[i])
        hour.append(st_date + time_add)
    # create dataframe

    res = zip(hour, time, distance, latlng, altitude, heartrate, velocity, pace, moving, cadence)
    res = list(res)

    df = pd.DataFrame(res,
                      columns=['hour', 'time', 'distance', 'latlng', 'altitude', 'heartrate', 'velocity(m/s)', 'pace',
                               'moving', 'cadence'])
    print(tipo_atv, hour[0].strftime('%H:%M %d/%m/%Y'))

    out = {'tipo_atv': tipo_atv, 'date': hour[0], 'dataset': df}
    return out


out = call_strava()