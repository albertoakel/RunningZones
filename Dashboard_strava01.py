
from running_functions import *
import matplotlib.pylab as plt
import time
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from running_functions import gpxfile_imp
from datetime import datetime, timedelta
import locale


locale.setlocale(locale.LC_TIME, "pt_BR.utf8")


#carregar_basededados
df = pd.read_parquet("data_base.parquet")  # Carregar

print('base de dados:')
print('Periodo:',df['date'][0],'-',df['date'].iloc[-1])
print('total de atividades:',df['date'].nunique())

lista_atv=df['date'].unique()
first_ocorr = df.drop_duplicates(subset='date', keep='first')
ind_first_ocorr = first_ocorr.index #indice_das_atividades

#criar DF com lista_atv
dfw = pd.DataFrame(lista_atv, columns=['data_atv'])
dfw['week'] = (pd.to_datetime(dfw['data_atv'], format='%d/%m/%Y-%H:%M')).dt.isocalendar().week
dfw['ano'] = (pd.to_datetime(dfw['data_atv'],format='%d/%m/%Y-%H:%M')).dt.year

atv_week = dfw.groupby(['ano', 'week'])['data_atv'].apply(list).reset_index()
atv_week.columns = ['ano', 'semana_do_ano', 'datas_da_semana']
#inverter ordem linhas
atv_week = atv_week.iloc[::-1].reset_index(drop=True)
#inverter ordem da lista dentro da coluna
atv_week['datas_da_semana'] = atv_week['datas_da_semana'].apply(lambda x: x[::-1])

print('Total semanas:',len(atv_week))
pd.set_option('display.max_row', None)
pd.set_option('display.max_colwidth', None)

fig, ax = plt.subplots()
for w in range(3):
    datas_da_semana = atv_week['datas_da_semana'][w]


 # Filtra os dados para toda a semana de uma vez
    for i in range(len(datas_da_semana)):
        ax.clear()
        data_e = [datas_da_semana[i]]
        df_temp = df[df['date'].isin(data_e)]
        #print(df_temp['date'].iloc[0][0:10])
        plt.plot(df_temp['distance'],df_temp['pace'])
        plt.title(df_temp['date'].iloc[0][0:10])
        plt.draw()  # Atualiza o gráfico
        plt.pause(0.1)  # Pausa para garantir que o gráfico seja exibido
        plt.waitforbuttonpress()




#plotar Volume
#Vol,Date_Vol=vol_week(df,atv_week,4)
# plt.bar(Date_Vol,Vol)
# plt.xticks(rotation=45,fontsize=8)
# plt.show()
#
print(df_temp)









