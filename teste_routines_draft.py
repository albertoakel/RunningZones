import pandas as pd

from running_functions import *

def sort_date_gpx():
    """
    program to test short in dataframe
    :return: sort date gpx file
    """

    z = pace_zones('4:08')
    path="/home/akel/Downloads/off_season2024"
    gpx_files = gpx_dir(path)
   #----------------------------------------
    temp_date=[]
    for i in range(len(gpx_files)):
        test=gpxfile_imp(path + '/'+gpx_files[i])
        temp_date.append(test['date'])
    #criando DF com nome da coluna
    A=pd.DataFrame(temp_date,columns=['datas'])
    print(A)
    print('---ordenado----')
    #ordenando pelo nome da coluna
    print(A.sort_values(by=['datas']))
    #---------------------------------------------------

    for i in range(len(gpx_files)):
        test=gpxfile_imp(path + '/'+gpx_files[i])
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



    dfn=df_0.sort_index(axis=1)
    print(dfn)
    for i in range(8):
        print(df_0.columns[i],dfn.columns[i])

    #print(df_0.columns[1],dfn.columns[1])
    #print(df_0.columns[2],dfn.columns[2])
    #print(df_0.columns[3],dfn.columns[3])

    dfa = pd.DataFrame({'col3': [1, 2, 4, np.nan, 'D', 'C'],
                    'col2': [2, 1, 9, 8, 7, 4],
                      'col1': [0, 1, 9, 4, 2, 3],
                      'col4': [5, 12, 1, 0, 192, 21]})

    dfb=dfa.sort_index(axis=1)
    print(dfb)
    # print(dfa.columns[0])
    # print(dfa.columns[1])
    # print(dfa.columns[2])
    # print(dfa.columns[3])