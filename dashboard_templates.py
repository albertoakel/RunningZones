import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from running_functions import gpxfile_imp


def dash_01():
    """
    examples
    https://plotly.com/python/line-charts/

    streamlit run main.py
    """
    #configuração da paginas
    st.set_page_config(layout="wide")

    #criar botão para leitura de arquivo
    opcoes2=('VDOT','FRIEL')

    #carregar lista de arquivos gpx


    option = st.selectbox("ESCOLHA SUA OPÇÃO",
            opcoes2,index=None)
    st.write("You selected:", option)
    if option== 'VDOT' :
        st.write('5 zonas de treino')
    elif option=='FRIEL':
        st.write('7 zonas de treino')
    else:
        pass

    path_files="/home/akel/Downloads/off_season2024"
    #gpx_files=gpx_dir(path_files)
    # try:
    #     dir_list = os.listdir(path_files)
    #     for file in dir_list:
    #         if file.endswith(".gpx"):
    #             gpx_files.append(file)
    #     if len(gpx_files) == 0:
    #         print('Não há arquivos GPX')
    #         return []
    # except FileNotFoundError:
    #     print(f"ERRO: O diretório '{path_files}' não foi encontrado.")
    #     return []

    #st.write(gpx_files)
    option = st.selectbox("ESCOLHA SUA OPÇÃO",
                          gpx_files, index=None)





def dash_02():
    """
    example botton and wiget
    :return:
    """
    import streamlit as st

    #opcoes1=[1.0,2,3,4,5,6]
    #opcoes2=('VDOT','FRIEL')
    # option = st.selectbox("ESCOLHA SUA OPÇÃO",
    #         opcoes2,index=None)
    # st.write("You selected:", option)
    # if option== 'VDOT' :
    #     st.write('5 zonas de treino')
    # elif option=='FRIEL':
    #     st.write('7 zonas de treino')
    # else:
    #     pass

    #2)
    out=[]
    with st.container(height=100):
        ftpa =st.text_input("pace ftpa:", "mm:ss")
        ts = pace_ts(ftpa)
        m_lim = ts // 60
        s_lim = ts % 60
        s = "%02d" % int(m_lim) + ':' + "%02d" % int(s_lim)
        percz = [[1.5, 1.292],
                 [1.292, 1.14],
                 [1.14, 1.06],
                 [1.06, 1],
                 [1, 0.97],
                 [0.97, 0.90],
                 [0.90, .85]]
        for j in range(0, len(percz)):
            ts_0 = ts * percz[j][0]
            ts_1 = ts * percz[j][1]
            s_0 = ts_0 % 60
            m_0 = ts_0 // 60
            s_1 = ts_1 % 60
            m_1 = ts_1 // 60
            S_0='0'+str(int(m_0))+':'+str(int(s_0))
            s_0 = "%02d" % int(m_0) + ':' + "%02d" % int(s_0)
            s_1 = "%02d" % int(m_1) + ':' + "%02d" % int(s_1)
            #st.write(s_0,s_1)
            out.append([s_0, s_1])
    #
    #st.write(out)
    #
    st.write('ZONAS DE TREINAMENTO BASEADO LIMIAR NO PACE LIMIAR LACTATO \nJoe Friel')
    st.write('Pace Limiar Lactato ~', s)
    st.write('Z1  ', out[0][1], out[0][0])
    st.write('Z2  ', out[1][1], out[1][0])
    st.write('Z3  ', out[2][1], out[2][0])
    st.write('Z4  ', out[3][1], out[3][0], '- Limiar lactato')
    st.write('Z5a ', out[4][1], out[4][0])
    st.write('Z5b ', out[5][1], out[5][0], ' -Zona Vo2')
    st.write('Z5c ', out[6][1], out[6][0], ' -Zona Anaeróbia ')
    # # else:
    # #     print('o que é :', opt + '?')
    #
    # return









