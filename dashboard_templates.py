from running_functions import *
import streamlit as st
#import pandas as pd
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

    col1, col2,col3 = st.columns([1, 4,1])

    #criar botão para leitura de arquivo
    #opcoes2=('VDOT','FRIEL')

    # carregar lista de arquivos gpx
    path_files = "/home/akel/Downloads/off_season2024"
    path_files="/home/akel/PycharmProjects/RunningZones/gpx_files/semanaFeb_3/"
    gpx_files = gpx_dir(path_files)

#coluna 1 # listar zonas de corrida by joe Friel
    with col1:
        ftpa = st.text_input("pace ftpa:","04:10")
        z = pace_zones(ftpa)
        st.markdown("###### zona 1:  " +z[0][1]+"  "+z[0][0])
        st.markdown("###### zona 2:  " +z[1][1]+"  "+z[1][0])
        st.markdown("###### zona 3:  " +z[2][1]+"  "+z[2][0])
        st.markdown("###### zona 4:  " +z[3][1]+"  "+z[3][0])
        st.markdown("###### zona 5a: " +z[4][1]+"  "+z[4][0])
        st.markdown("###### zona 5b: " +z[5][1]+"  "+z[5][0])
        st.markdown("###### zona 5c: " +z[6][1]+"  "+z[6][0])


# coluna 2 e 3 e 4 # volume total treinado na semana.
    df_0=gpxfiles_df(path_files,ftpa) #read files, sort by date and create dataframe
    pd.set_option('display.max_row', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)
    print('shape df_0', df_0.shape)
    print(df_0)
    sz=df_0.shape

    x=df_0.columns[0:sz[1]]
    #y=df_0.loc[1, df_0.columns[0:sz[1]]]
    #print(y)
   #cores = ['purple','darkblue','cadetblue','orange','chocolate','red','darkred']
    cores = {0:'purple',1:'darkblue',2: 'cadetblue',3:'orange',4:'chocolate',5:'red',6:'darkred'}
    # stack-bar_volume
    fig1 = go.Figure()
    zone_name = ['z1', 'z2', 'z3', 'z4', 'z5a', 'z5b', 'z5c']
    for i in range(len(zone_name)) :
        fig1.add_trace(go.Bar(
            name=zone_name[i],
            x=x,
            y=df_0.loc[i, df_0.columns[0:sz[1]]],
            marker_color=cores[i],
            text = df_0.loc[i, df_0.columns[0:sz[1]]].round(2).tolist(),  # Adicionando os valores como texto nas barras
            textposition='inside',  # Posicionando o texto dentro da barra
            hoverinfo='text',
                             ))
    #text = df_0.loc[i, df_0.columns[0:sz[1]]].round(2).tolist()
    #text = list(round(df_0.loc[i, df_0.columns[0:sz[1]]]))
    fig1.update_layout(
    barmode='stack',
    title="Volume semanal",
    xaxis_title="Categorias",
    yaxis_title="Valores",
    yaxis=dict(range=[0, 105]),
    legend_title="Zonas")
    with col2:
        st.plotly_chart(fig1)


    #grafico de pizza
    out=vol_zone(path_files,ftpa)
    znp=out['p_zones']

    df_zones=pd.DataFrame(zone_name,columns=['zone_name'])
    df_zones['perc_zones']=znp[2:9]

    option = st.selectbox("ESCOLHA SUA OPÇÃO",gpx_files, index=0)
    out = gpxfile_imp(path_files + '/' + str(option))

    d=out['d']
    p=out['p']
    t=out['t']

    #d2 = out['df']['distance'].values.tolist()
    #p2 = out['df']['pace'].values.tolist()
    #t2 = out['df']['time(s)'].to_numpy(dtype='float32')

    zn=find_zones(p,t,d,z)
    z1  = zn['id1']
    z2  = zn['id2']
    z3  = zn['id3']
    z4  = zn['id4']
    z5a = zn['id5a']
    z5b = zn['id5b']
    z5c = zn['id5c']
    pzn = zn['p_zones']


    #dataset = pd.DataFrame({'d': d, 'p': p, 't': t})

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=d, y=p,
                              mode='lines',line_color='silver',
                              name='pace'))
    #adcionar zonas
    fig2.add_trace(go.Scatter(x=d[z1], y=p[z1],
                               mode='markers',line_width = 1,
                               marker=dict(color='purple'),
                             name='Z1 '+ '%05.2f'%(pzn[2]*100) + '%'))
    fig2.add_trace(go.Scatter(x=d[z2], y=p[z2],
                              mode='markers', line_width=1,
                              marker=dict(color='darkblue'),
                              name='Z2 '+ '%05.2f'%(pzn[3]*100) + '%'))
    fig2.add_trace(go.Scatter(x=d[z3], y=p[z3],
                              mode='markers', line_width=1,
                              marker=dict(color='cadetblue'),
                              name='Z3 '+ '%05.2f'%(pzn[4]*100) + '%'))
    fig2.add_trace(go.Scatter(x=d[z4], y=p[z4],
                              mode='markers', line_width=1,
                              marker=dict(color='orange'),
                              name='Z4 '+ '%05.2f'%(pzn[5]*100) + '%'))
    fig2.add_trace(go.Scatter(x=d[z5a], y=p[z5a],
                              mode='markers', line_width=1,
                              marker=dict(color='chocolate'),
                              name='Z5a '+ '%05.2f'%(pzn[6]*100) + '%'))
    fig2.add_trace(go.Scatter(x=d[z5b], y=p[z5b],
                              mode='markers', line_width=1,
                              marker=dict(color='red'),
                              name='Z5b '+ '%05.2f'%(pzn[7]*100) + '%'))
    fig2.add_trace(go.Scatter(x=d[z5c], y=p[z5c],
                              mode='markers', line_width=1,
                              marker=dict(color='darkred'),
                              name='Z5c '+ '%05.2f'%(pzn[8]*100) + '%'))
    fig2.update_layout(xaxis_range=[0, d[-1]])
    fig2.update_layout(yaxis_range=[7, 3.5])

    with st.container():

        st.plotly_chart(fig2, use_container_width=True)


    fig3= px.pie(df_zones, values='perc_zones', names='zone_name',color='zone_name',
                 color_discrete_map={'z1': cores[0],
                                     'z2': cores[1],
                                     'z3': cores[2],
                                     'z4': cores[3],
                                     'z5a': cores[4],
                                     'z5b': cores[5],
                                     'z5c': cores[6]})
    fig3.update_traces(textposition='inside')
    fig3.update_layout(showlegend=False)

    with col3:
        st.plotly_chart(fig3)

