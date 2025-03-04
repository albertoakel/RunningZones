import pandas as pd
import numpy as np
import time

#leitura dos arquivos
# df1 = pd.read_parquet("file_strava.04-03-2025-20-12-2024.parquet")  # Carregar
# df2 = pd.read_parquet("file_strava.18-12-2024-22-10-2024.parquet")  # Carregar
#
# #contatenar e mudar coluna
# DF = pd.concat([df1, df2], ignore_index=True)
# DF.rename(columns={"dataset": "date"}, inplace=True)
#
# #filename e salvar
# filename='file_strava.'+DF['date'][0][0:10]+'-'+DF['date'][len(DF)-1][0:10]+'.parquet'
# filename = filename.replace("/", "-")
# print(filename)
# DF.to_parquet(filename, index=False)  # Salvar



df_teste = pd.read_parquet("file_strava.04-03-2025-22-10-2024.parquet")  # Carregar

print(df_teste['date'][0][0:10])
print(df_teste['date'][0],df_teste['date'][len(df_teste)-1])

#print(df_teste)