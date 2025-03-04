#usando dicionarios
import pandas as pd
import numpy as np
import time

# Número de DataFrames a serem gerados
num_dfs = 100
num_linhas = 2000

# 🔹 Método 1: Usando lista + concat (Melhor abordagem)
start = time.time()
# Criando um dicionário vazio para armazenar os DataFrames
dataframes = {}

# Gerando múltiplos DataFrames e armazenando no dicionário
for i in range(num_dfs):  # Exemplo com 3 DataFrames
    df = pd.DataFrame({
        "tempo": np.random.randint(300, 3600, num_linhas),
        "velocidade": np.random.uniform(2, 15, num_linhas),
        "altimetria": np.random.randint(-50, 500, num_linhas)
    })
    dataframes[f"df_{i+1}"] = df  # Armazena com uma chave nomeada

df_geral = pd.concat([df.assign(dataset=name) for name, df in dataframes.items()], ignore_index=True)

# Acessando um DataFrame específico
tempo_concat = time.time() - start
print(f"Lista + concat: {tempo_concat:.5f} segundos")
print(df_geral.shape)
df_geral.to_parquet("dados.parquet", index=False)  # Salvar
#df_geral.to_hdf("dados.h5", key="dataset", mode="w")  # Salvar

