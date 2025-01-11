from pandas import wide_to_long

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
    st.markdown("## Running functions ")

    #criar botão para leitura de arquivo
    opcoes2=('VDOT','FRIEL')


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


    #carregar lista de arquivos gpx
    #path_files="/home/akel/Downloads/off_season2024"
    path_files="/home/akel/codigos _python/"
    gpx_files=gpx_dir(path_files)
# -------------------------------------------------
# começa aqui
    Z_st = ['z1', 'z2', 'z3', 'z4', 'z5a', 'z5b', 'z5c']
    #df_0 = pd.DataFrame({'zones%': Z_st})
    for i in range(len(gpx_files)):
        test=gpxfile_imp(path_files + '/'+gpx_files[i])
        d_o = test['d']
        p_o = test['p']
        t_o = test['t']
        j1,j2,j3,j4,j5a,j5b,j5c=find_zones(p_o, t_o, d_o, z)
        temp_date=test['date']
        total=len(p_o[j1])+len(p_o[j2])+len(p_o[j3])+len(p_o[j4])+len(p_o[j5a])+len(p_o[j5b])+len(p_o[j5c])
        z1_o = (len(p_o[j1])/ total * 100)
        z2_o = (len(p_o[j2])/ total * 100)
        z3_o = (len(p_o[j3])/ total * 100)
        z4_o = (len(p_o[j4])/ total * 100)
        z5a_o = (len(p_o[j5a])/ total * 100)
        z5b_o = (len(p_o[j5b])/ total * 100)
        z5c_o = (len(p_o[j5c])/ total * 100)
        zones=[z1_o,z2_o,z3_o,z4_o,z5a_o,z5b_o,z5c_o]
        if i==0:
            df_0 = pd.DataFrame({temp_date.strftime("%d/%m/%Y"): zones})
        else:
            df_n=pd.DataFrame({temp_date.strftime("%d/%m/%Y"): zones})
            df_0=pd.concat([df_0,df_n],axis=1)

    x=df_0.columns[0:8]
    y=df_0.loc[1, df_0.columns[0:8]]

    # stackbar_volume_week
    fig = go.Figure()
    zone_name = ['z1', 'z2', 'z3', 'z4', 'z5a', 'z5b', 'z5c']
    for i in range(len(zone_name)) :
        fig.add_trace(go.Bar(name=zone_name[i],x=x, y=df_0.loc[i, df_0.columns[0:8]],
                             text=list(round(df_0.loc[i, df_0.columns[0:8]])),  # Adicionando os valores como texto nas barras
                             textposition='inside',  # Posicionando o texto dentro da barra
                             hoverinfo='text'
                             ))
    fig.update_layout(
    barmode='stack',
    title="Volume semanal",
    xaxis_title="Categorias",
    yaxis_title="Valores",
    yaxis=dict(range=[0, 105]),
    legend_title="Zonas")


    with col2:
        st.plotly_chart(fig)
#termina aqui
#-----------------------
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


    K=df_0.T
    st.write(K)


