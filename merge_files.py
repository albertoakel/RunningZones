import pandas as pd

import numpy as np
import time

#leitura dos arquivos
df1 = pd.read_parquet("file_strava.06-03-2025-06-03-2025.parquet")  # data mais recente
df2 = pd.read_parquet("data_base.parquet")  # data mais antiga
# # file_strava.27-12-2023-07-10-2023.parquet
# # #contatenar e mudar coluna
print(df1['date'].iloc[0])
print(df1['date'].iloc[-1],len(df1))
print(df2['date'].iloc[0])
print(df2['date'].iloc[-1],len(df2))
print('total:',len(df1)+len(df2))
#
DF = pd.concat([df1, df2], ignore_index=True)
print(DF['date'].iloc[0])
print(DF['date'].iloc[-1],len(DF))
# # #
# # #filename e salvar
filename='file_strava.'+DF['date'][0][0:10]+'-'+DF['date'][len(DF)-1][0:10]+'.parquet'
filename = filename.replace("/", "-")
print(filename,DF.shape )


while True:
    resposta1 = input("Todas informações estão corretas. pronto pra salvar(s/n): ").strip().lower()
    if resposta1 == 's':
        resposta2 = input("Confirme novamente (s/n): ").strip().lower()
        if resposta2 == 's':
            DF.to_parquet(filename, index=False)  # Salvar
            print("Ação confirmada! 🚀")
            break
        else:
            print("Ação cancelada na segunda confirmação. ❌")
            break
    elif resposta1 == 'n':
        print("Ação cancelada! ❌")
        break
    else:
        print("Opção inválida! Digite 's' para sim ou 'n' para não.")


