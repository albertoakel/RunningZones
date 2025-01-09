
from running_functions import *
import streamlit as st
import pandas as pd
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
    st.markdown("## Running functions"+'sads')

    #criar botão para leitura de arquivo
    opcoes2=('VDOT','FRIEL')

    #carregar lista de arquivos gpx
    col1,col2=st.columns([1,3])
    with col1:
        ftpa = st.text_input("pace ftpa:","04:10")
        z = pace_zones(ftpa)
        st.markdown("##### zona 1:  " +z[0][1]+"  "+z[0][0])
        st.markdown("##### zona 2:  " +z[1][1]+"  "+z[1][0])
        st.markdown("##### zona 3:  " +z[2][1]+"  "+z[2][0])
        st.markdown("##### zona 4:  " +z[3][1]+"  "+z[3][0])
        st.markdown("##### zona 5a: " +z[4][1]+"  "+z[4][0])
        st.markdown("##### zona 5b: " +z[5][1]+"  "+z[5][0])
        st.markdown("##### zona 5c: " +z[6][1]+"  "+z[6][0])

    with col2:
        st.markdown("## nasdasssssssssssssssssss asfdasifh fahdf hasfdhsa sdf sadfbsgd")







    #path_files="/home/akel/Downloads/off_season2024"
    path_files="/home/akel/codigos _python/"
    gpx_files=gpx_dir(path_files)

    option = st.selectbox("ESCOLHA SUA OPÇÃO",gpx_files, index=0)
    out = gpxfile_imp(path_files + '/' + str(option))

    d=out['d']
    p=out['p']
    t=out['t']

    z1,z2,z3,z4,z5a,z5b,z5c=find_zones(p,t,d,z)

    dataset = pd.DataFrame({'d': d, 'p': p, 't': t})

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=d, y=p,
                              mode='lines',line_color='silver',
                              name='pace'))
    #adcionar zonas
    fig1.add_trace(go.Scatter(x=d[z1], y=p[z1],
                               mode='markers',line_width = 1,
                               marker=dict(color='purple'),
                             name='Z1'))
    fig1.add_trace(go.Scatter(x=d[z2], y=p[z2],
                              mode='markers', line_width=1,
                              marker=dict(color='darkblue'),
                              name='Z2'))
    fig1.add_trace(go.Scatter(x=d[z3], y=p[z3],
                              mode='markers', line_width=1,
                              marker=dict(color='cadetblue'),
                              name='Z3 - marathon'))
    fig1.add_trace(go.Scatter(x=d[z4], y=p[z4],
                              mode='markers', line_width=1,
                              marker=dict(color='orange'),
                              name='Z4 - threshold'))
    fig1.add_trace(go.Scatter(x=d[z5a], y=p[z5a],
                              mode='markers', line_width=1,
                              marker=dict(color='chocolate'),
                              name='Z5a'))
    fig1.add_trace(go.Scatter(x=d[z5b], y=p[z5b],
                              mode='markers', line_width=1,
                              marker=dict(color='red'),
                              name='Z5b'))
    fig1.add_trace(go.Scatter(x=d[z5c], y=p[z5c],
                              mode='markers', line_width=1,
                              marker=dict(color='darkred'),
                              name='Z5c'))
    fig1.update_layout(xaxis_range=[0, d[-1]])
    fig1.update_layout(yaxis_range=[3.5, 7])

    with st.container():
        st.plotly_chart(fig1, use_container_width=True)






