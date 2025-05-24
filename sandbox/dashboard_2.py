from running_functions import *
import streamlit as st
#import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from running_functions import gpxfile_imp


def dash_02():
    """
    examples
    https://plotly.com/python/line-charts/
    streamlit run main.py
    """

    #configuração da paginas
    st.set_page_config(layout="wide")
    st.markdown("## Running round 2")
    col1, col2,col3 = st.columns([1, 4,1])

    # leitura_dados
    df = pd.read_parquet("data_base.parquet")  # Carregar
    atv_week, list_atv = data_week(df)

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

    path_files="/home/akel/PycharmProjects/RunningZones/gpx_files/semanaFeb_3/"
    gpx_files = gpx_dir(path_files)
    df_0=gpxfiles_df(path_files,ftpa) #read files, sort by date and create dataframe

    sz=df_0.shape

    x=df_0.columns[0:sz[1]]                   #é a datas da semana
    y=df_0.loc[1, df_0.columns[0:sz[1]]]      #percentual_volume_na_zona
    pd.set_option('display.max_row', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)
    print('shape df_0', df_0.shape)
    print('shape', x.shape)
    print('shape', y.shape)
    print(df_0)

