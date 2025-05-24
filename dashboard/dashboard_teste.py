import sys
from pathlib import Path

# Adiciona o diretório src ao PATH
# Detecta ambiente (local vs. Streamlit Cloud)
is_streamlit_cloud = "streamlit" in str(Path.cwd())

# Configura caminhos dinamicamente
if is_streamlit_cloud:
    sys.path.append(str(Path(__file__).parent / "src"))  # Caminho no deploy
else:
    sys.path.append(str(Path(__file__).parent.parent / "src"))  # Caminho local

from running_functions import *
import streamlit as st
import plotly.graph_objects as go
from running_functions import gpxfile_imp
import tempfile


# Configuração da página
st.set_page_config(page_title="Analisador de Zonas em Corridas", layout="wide")

# Título centralizado
st.markdown("<h1 style='text-align: center;'>Analisador de Zonas em Corridas</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    ftpa = st.text_input("pace ftpa(limiar) :", "04:10")
    z = pace_zones(ftpa)
    st.markdown("###### zona 1:  " + z[0][1] + "  " + z[0][0])
    st.markdown("###### zona 2:  " + z[1][1] + "  " + z[1][0])
    st.markdown("###### zona 3:  " + z[2][1] + "  " + z[2][0])
    st.markdown("###### zona 4:  " + z[3][1] + "  " + z[3][0])
    st.markdown("###### zona 5a: " + z[4][1] + "  " + z[4][0])
    st.markdown("###### zona 5b: " + z[5][1] + "  " + z[5][0])
    st.markdown("###### zona 5c: " + z[6][1] + "  " + z[6][0])

# Linha para upload de arquivo GPX
with col2:
    uploaded_file = st.file_uploader("Escolha um arquivo GPX", type=["gpx"])

    if uploaded_file is not None:
        try:
            # Cria arquivo temporário para a função que espera um caminho
            with tempfile.NamedTemporaryFile(delete=False, suffix=".gpx") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            # Processa o GPX com sua função
            out = gpxfile_imp(tmp_path)

            d = out['d']
            p = out['p']
            t = out['t']
            zn = find_zones(p, t, d, z)
            z1 = zn['id1']
            z2 = zn['id2']
            z3 = zn['id3']
            z4 = zn['id4']
            z5a = zn['id5a']
            z5b = zn['id5b']
            z5c = zn['id5c']
            pzn = zn['p_zones']

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=d, y=p,
                                      mode='lines', line_color='silver',
                                      name='pace'))
            # adcionar zonas
            fig2.add_trace(go.Scatter(x=d[z1], y=p[z1],
                                      mode='markers', line_width=1,
                                      marker=dict(color='purple'),
                                      name='Z1 ' + '%05.2f' % (pzn[2] * 100) + '%'))
            fig2.add_trace(go.Scatter(x=d[z2], y=p[z2],
                                      mode='markers', line_width=1,
                                      marker=dict(color='darkblue'),
                                      name='Z2 ' + '%05.2f' % (pzn[3] * 100) + '%'))
            fig2.add_trace(go.Scatter(x=d[z3], y=p[z3],
                                      mode='markers', line_width=1,
                                      marker=dict(color='cadetblue'),
                                      name='Z3 ' + '%05.2f' % (pzn[4] * 100) + '%'))
            fig2.add_trace(go.Scatter(x=d[z4], y=p[z4],
                                      mode='markers', line_width=1,
                                      marker=dict(color='orange'),
                                      name='Z4 ' + '%05.2f' % (pzn[5] * 100) + '%'))
            fig2.add_trace(go.Scatter(x=d[z5a], y=p[z5a],
                                      mode='markers', line_width=1,
                                      marker=dict(color='chocolate'),
                                      name='Z5a ' + '%05.2f' % (pzn[6] * 100) + '%'))
            fig2.add_trace(go.Scatter(x=d[z5b], y=p[z5b],
                                      mode='markers', line_width=1,
                                      marker=dict(color='red'),
                                      name='Z5b ' + '%05.2f' % (pzn[7] * 100) + '%'))
            fig2.add_trace(go.Scatter(x=d[z5c], y=p[z5c],
                                      mode='markers', line_width=1,
                                      marker=dict(color='darkred'),
                                      name='Z5c ' + '%05.2f' % (pzn[8] * 100) + '%'))
            fig2.update_layout(xaxis_range=[0, d[-1]])
            fig2.update_layout(yaxis_range=[7, 3.5])

            with st.container():

                st.plotly_chart(fig2, use_container_width=True)


        except Exception as e:
            st.error(f"Erro ao processar o arquivo GPX: {e}")
    else:
        st.info("Por favor, envie um arquivo GPX para começar.")

with col2: # Ou 'with col3:' se preferir outra coluna
    st.markdown("---") # Adiciona uma linha horizontal para separar visualmente
    with st.expander("Clique para ver os Detalhes Técnicos do Código"):
        st.markdown("""

    **Este aplicativo Streamlit permite avaliar as zonas de corridas a parti da leitura dos arquivos gpx( veja no strava)**

    Usamos a abordagem identificar o Pace de limiar funcional (FTPA) definido por joel Friel. 
    Detalhes vc encontra aqui. https://joefrieltraining.com/a-quick-guide-to-setting-zone/

    ##### ⚙️ Testes para Estimativa do Ritmo de Limiar (FTPa)                   
    ###### 🕒 Teste de 20 minutos
    - Corra 20 minutos em ritmo forte e controlado.
    - Calcule o ritmo médio e aplique um ajuste de 5% (adicione ~13 segundos por km).

    **Exemplo:**
    - Ritmo médio: `4:30 min/km`  
    - Ajuste de 5%: `+0:13`  
    - **Ritmo estimado de limiar:** `4:43 min/km`

    ###### 🕒 Teste de 30 minutos
    - Corra 30 minutos em ritmo forte e constante.
    - O ritmo médio será o próprio **ritmo de limiar**.

    **Exemplo:**
    - Ritmo médio: `4:45 min/km`  
    - **Ritmo estimado de limiar:** `4:45 min/km`

    ###### 📌 Qual escolher?
    - **20 minutos:** mais adequado para quem treina em alta intensidade. O ajuste compensa o tempo reduzido.
    - **30 minutos:** mais direto e confiável, ideal para quem sustenta ritmo alto por mais tempo.

    """)
