import os

from click import option

from running_functions import *
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

    ftpa = st.text_input("pace ftpa:", "mm:ss")
    st.write('FTPA:', ftpa)
    #z = pace_zones(ftpa)


    path_files="/home/akel/Downloads/off_season2024"
    gpx_files=gpx_dir(path_files)

   # option = st.selectbox("ESCOLHA SUA OPÇÃO", ["Nenhum"] + gpx_files)

    # Mostra o arquivo selecionado

    option = st.selectbox("ESCOLHA SUA OPÇÃO",gpx_files, index=0)
    st.write('seu arquivo é:',option)

    out = gpxfile_imp(path_files + '/' + str(option))

    d=out['d']
    p=out['p']
    t=out['t']
    #st.write(d[0:10])

    dataset = pd.DataFrame({'d': d, 'p': p, 't': t})
    # with st.container(height=400):
    #     st.line_chart(dataset,x='d', y="p")
    #with st.container(height=400):
    col1,col2,col3=st.columns([1,8,1])

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=d, y=p,
                              mode='lines',line_color='#999791',
                              name='pace',fillcolor='red'))
    fig1.add_trace(go.Scatter(x=d, y=p,
                              mode='markers',line_width = 1,
                              marker=dict(color='blue'),
                            name='markers'))
    col2.plotly_chart(fig1)




    #find_zones(p, t, d, z)

    # This is the document title




