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

    option = st.selectbox("ESCOLHA SUA OPÇÃO",gpx_files, index=None)

    st.write('seu arquivo é:',option)
    if str(option) != "None":
        out = gpxfile_imp(path_files + '/' + str(option))
    else:
        pass

    t = out['t']
    d = out['d']
    p = out['p']
    st.write(d[-1])
    st.write(t[-1])

    #find_zones(p, t, d, z)

    # This is the document title




