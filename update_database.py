
from running_functions import *


#leitura dos arquivos
df1 = pd.read_parquet("file_strava.06-03-2025-21-02-2025.parquet")  # data mais recente
filebase='data_base.parquet'
df2 = pd.read_parquet(filebase)  # data mais antiga



print(df1['date'].iloc[0])
print(df1['date'].iloc[-1],len(df1))
print(df2['date'].iloc[0])
print(df2['date'].iloc[-1],len(df2))
print('total:',len(df1)+len(df2))
#
DF = pd.concat([df1, df2], ignore_index=True)
DF.drop_duplicates(subset=['date','distance','time','cadence','week'],inplace=True) #remover duplicadas
DF.reset_index(drop=True, inplace=True) #resetar indices
print(filebase,DF.shape )


while True:
    resposta1 = input("Todas informações estão corretas. pronto pra salvar(s/n): ").strip().lower()
    if resposta1 == 's':
        resposta2 = input("Confirme novamente (s/n): ").strip().lower()
        if resposta2 == 's':
            DF.to_parquet(filebase, index=False)  # Salvar
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
