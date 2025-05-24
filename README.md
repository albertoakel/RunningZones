# 🏃‍♂️ Dashboard de Desempenho para Corrida

Este projeto tem como objetivo o desenvolvimento de um **dashboard interativo em Streamlit** voltado para **análise de métricas de desempenho de corrida**, com possibilidade de integração com **APIs como Strava ou Garmin**. O sistema é voltado para atletas, treinadores e entusiastas que desejam acompanhar sua evolução e entender melhor sua performance.

## 🎯 Funcionalidades

- Visualização de métricas como pace, distância, frequência cardíaca, altimetria e zonas de esforço
- Cálculo automatizado de **ritmo de limiar funcional (FTPa)** baseado em testes de campo
- Implementação de testes de desempenho como:
  - Teste de 20 minutos com ajuste de 5%
  - Teste de 30 minutos
  - Testes com base no VDOT (3 km e 5 km)
- Interface intuitiva com visualização gráfica e dashboards interativos no Streamlit
- (Em desenvolvimento) Integração com **Strava** e **Garmin Connect**

## 📊 Prévia da Interface (Streamlit)

*(Adicione aqui prints da interface ou link para versão online do Streamlit, se disponível)*

## ⚙️ Testes para Estimativa do Ritmo de Limiar (FTPa)

### 🕒 Teste de 20 minutos
- Corra 20 minutos em ritmo forte e controlado.
- Calcule o ritmo médio e aplique um ajuste de 5% (adicione ~13 segundos por km).

**Exemplo:**
- Ritmo médio: `4:30 min/km`  
- Ajuste de 5%: `+0:13`  
- **Ritmo estimado de limiar:** `4:43 min/km`

### 🕒 Teste de 30 minutos
- Corra 30 minutos em ritmo forte e constante.
- O ritmo médio será o próprio **ritmo de limiar**.

**Exemplo:**
- Ritmo médio: `4:45 min/km`  
- **Ritmo estimado de limiar:** `4:45 min/km`

### 📌 Qual escolher?
- **20 minutos:** mais adequado para quem treina em alta intensidade. O ajuste compensa o tempo reduzido.
- **30 minutos:** mais direto e confiável, ideal para quem sustenta ritmo alto por mais tempo.

## 📐 Testes de Desempenho com VDOT

### 📏 Teste de 3 km
- Avaliação de VO₂máx e ritmo competitivo baseado em tempo para 3 km.

### 📏 Teste de 5 km
- Estimativa de performance em distâncias maiores, zonas de treino e tempo-alvo em provas.

---

## 📁 Estrutura do Projeto
```
📦 run-metrics-dashboard/
├── 📂 src/ # Funções para cálculo de ritmo e FTP
├── 📂 data/ # Dados de treino (Strava, Garmin, CSV)
├── 📂 dashboard/ # Código do Streamlit
├── 📂 sandbox/ # Protótipos e experimentos
└── README.md
```


---

## 🔧 Requisitos

Crie um ambiente Conda e instale os pacotes com:

```bash
conda create -n run-metrics python=3.10
conda activate run-metrics
pip install -r requirements.txt
```

## 🌍 English Summary

**Run Metrics Dashboard** is a Streamlit-based interactive dashboard for analyzing running performance.  
It supports:

- Threshold pace estimation (20-min & 30-min tests)
- VDOT-based 3 km & 5 km tests
- Interactive metric visualizations
- Planned integration with **Strava** and **Garmin** APIs

> Ideal for runners, coaches, and data scientists exploring endurance analytics.

---

## 📬 Contribuições

**Contribuições são bem-vindas!**  
Você pode:

- 🔧 Abrir uma issue para sugerir melhorias ou reportar bugs
- 🚀 Criar um pull request com novas funcionalidades
- 💡 Compartilhar ideias para integração com outras plataformas
