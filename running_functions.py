"""
A set of functions for running evaluation and performance

"""
import matplotlib.pyplot as plt
import numpy as np
import os


def ts_pace(ts):
    """
    convert time in second to pace(string)
    :param ts: time in second
    :return: pace (string)
    """
    s = ts % 60
    m = ts // 60
    pace = "%02d" % int(m) + ':' + "%02d" % int(s)  # string
    return pace
def pp_pace(time):
    """
    convert time decimal to pace(string) min:secondo
    :param time:
    :return:
    """
    return ts_pace(time*60)
def pace_ts(time):
    """
    convert pace or time (string in format mm:ss) to time in second
    :param time:
    :return:
    """
    if len(time) == 4:
        m = time[0:1]
        s = time[2:4]
    elif len(time)==5:
        m = time[0:2]
        s = time[3:5]
    else:
        m = time[0:3]
        s = time[4:5]

    m = int(m)
    s = int(s)

    return m*60 + s

def gpx_dir(path_files):

    gpx_files = []
    try:
        dir_list = os.listdir(path_files)
        for file in dir_list:
            if file.endswith(".gpx"):
                gpx_files.append(file)
        if len(gpx_files) == 0:
            print('Não há arquivos GPX')
            return []
    except FileNotFoundError:
        print(f"ERRO: O diretório '{path_files}' não foi encontrado.")
        return []

    return gpx_files

def pace_zones(ftpa,**kwargs):
    """
    Created on Sun Dec 15 14:32:43 2024

    @author: akel

    Pace zones by joel friel. You need find your Functional
    Threshold Pace

    https://joefrieltraining.com/a-quick-guide-to-setting-zone/

    Functional Threshold Pace (FTPa)
    These two options are common methods to estimate the lactate
    threshold (LT) or threshold pace, especially for runners who want
    to adjust their training based on effort zones.

    Option 1) - 20-Minute Run:

    Run for 20 minutes at a strong but sustainable pace. At the end, calculate
    your average pace. Multiply the average
    pace by 1.05 (or add 5% to the time per kilometer). The result will be your estimated threshold pace.
    Example:
    Average pace over 20 minutes: 4:30 min/km. 5% of 4:30 is about 0:13 seconds.
    Estimated threshold:'ftpa' f4:43 min/km.

    Option 2) - 30-Minute Run:
    Run for 30 minutes at a strong but steady pace. Calculate the average pace
    during this period. This average pace will be your threshold directly,
    with no adjustments needed.
    #Example:
    Average pace over 30 minutes: 4:45 min/km.
    Threshold: 4:45 min/km.
    Which one to choose?
    20-Minute Run: A good option if you're already used to running at high intensity and can maintain a strong pace in a controlled manner. The 5% adjustment compensates for the shorter test duration.
    30-Minute Run: Ideal for those who prefer a more straightforward method and are willing to sustain a strong pace for a longer period.
    Both methods provide a good estimate and can be used to guide interval training or effort-based zones. Have you tried either of these methods?

    :param ftpa: Functional Threshold Pace (FTPa)
    :param kwargs: opt=print. print zones in terminal
    :return: 7 running zones
    """
    opt = kwargs.get('opt')
    out = []
    ts=pace_ts(ftpa)
    s_lim = ts % 60
    m_lim = ts // 60
    s = "%02d" % int(m_lim) + ':' + "%02d" % int(s_lim)


    percz = [[1.5, 1.292],
         [1.292, 1.14],
         [1.14, 1.06],
         [1.06, 1],
         [1, 0.97],
         [0.97, 0.90],
         [0.90, .85]]
    for i in range(0, len(percz )):
        #        ts_0=ts/((Z[i][0])*0.01)
        ts_0 = ts * percz [i][0]
        ts_1 = ts * percz [i][1]
        s_0 = ts_0 % 60
        m_0 = ts_0 // 60
        s_1 = ts_1 % 60
        m_1 = ts_1 // 60
        #        S_0='0'+str(int(m_0))+':'+str(int(s_0))
        s_0 = "%02d" % int(m_0) + ':' + "%02d" % int(s_0)
        s_1 = "%02d" % int(m_1) + ':' + "%02d" % int(s_1)
        out.append([s_0, s_1])

    if opt is None:
        pass
    elif (opt.lower()) == 'print':
        print('ZONAS DE TREINAMENTO BASEADO LIMIAR NO PACE LIMIAR LACTATO \nJoe Friel')
        print('Pace Limiar Lactato ~', s)
        print('---------------------------------------')
        print('Z1  ', out[0][1], out[0][0])
        print('Z2  ', out[1][1], out[1][0])
        print('Z3  ', out[2][1], out[2][0])
        print('Z4  ', out[3][1], out[3][0], '- Limiar lactato')
        print('Z5a ', out[4][1], out[4][0])
        print('Z5b ', out[5][1], out[5][0], ' -Zona Vo2')
        print('Z5c ', out[6][1], out[6][0], ' -Zona Anaeróbia ')
    else:
        print( 'o que é :', opt +'?')

    return out


def vdot3km(t3km,**kwargs):
    """
    Pace zones by jack daniel(Vdot).

    :param t3km: time('mm:ss') for 3 km test.
    :param kwargs: opt=print. print zones in terminal
    :return: zones by v.dot
    """
    print('')
    print('ZONAS DE TREINAMENTO Vdot')
    print('Tempo de corrida 3km', t3km)
    print('-----')
    opt = kwargs.get('opt')
    # coeficientes para 3km
    tm = ([[1, 12], [1, 15]])
    ts_z1a = ([[350], [422]])
    ts_z1b = ([[318], [384]])
    ts_z2 = ([[281], [348]])
    ts_z3 = ([[265], [323]])
    ts_z4 = ([[243], [295]])
    ts_z5 = ([[228], [280]])
    cz1a = np.linalg.solve(tm, ts_z1a)
    cz1b = np.linalg.solve(tm, ts_z1b)
    cz2 = np.linalg.solve(tm, ts_z2)
    cz3 = np.linalg.solve(tm, ts_z3)
    cz4 = np.linalg.solve(tm, ts_z4)
    cz5 = np.linalg.solve(tm, ts_z5)
    t3km=pace_ts(t3km) /60 #convert time minute decimal mm.ss
    pz1a = cz1a[1]*t3km + cz1a[0]
    pz1b = cz1b[1]*t3km + cz1b[0]-6
    pz2 = cz2[1]*t3km + cz2[0]
    pz3 = cz3[1]*t3km + cz3[0]
    pz4 = cz4[1]*t3km + cz4[0]
    pz5 = cz5[1]*t3km + cz5[0]
    if opt is None:
        pass
    elif (opt.lower()) == 'print':
        print('Z1', 'Corrida leve   ', ts_pace(pz1b), ts_pace(pz1a))
        print('Z2', 'Endurance      ', ts_pace(pz2),ts_pace(pz2+15))
        print('Z3', 'Limiar         ', ts_pace(pz3),ts_pace(pz3+15))
        print('Z4', 'Vo2            ', ts_pace(pz4),ts_pace(pz4+15))
        print('Z5', 'Anaeróbico     ', ts_pace(pz5),ts_pace(pz5+15))
        print('Z5a', 'morte         ', ts_pace(pz5 * 0.922))
    else:
        print( 'o que é :', opt +'?')
    out= [[pz1b, pz1a], [pz2, pz2 + 15], [pz3, pz3 + 15], [pz4, pz4 + 15], [pz5, pz5 + 15], [pz5 * 0.85, pz5 * 0.922]]

    return out
def gpxfile_imp(filegpx,**kwargs):
    """
    :param filegpx: Extract data info of gpx file from strava
    :return: time,distance e pace
    """

    import gpxpy.gpx
    from datetime import timezone, timedelta
    from haversine import haversine
    opt = kwargs.get('opt')
    if opt is None:
        pass
    plt.close('all')

    gpx_file = open(filegpx, 'r')
    gpx0 = gpxpy.parse(gpx_file)

    #moving_data = gpx0.get_moving_data(raw=True)
    #print(moving_data)


    hr = []  #  batimento cardíaco
    lat = []  # latitude
    lon = []  # longitude
    ele = []  # elevação
    t = []  # datetime_instante
    n = len(gpx0.tracks[0].segments[0].points)
    #print(gpx0.time) #dia/hora da atividade
    for i in range(0, n, 1):
        temp= gpx0.tracks[0].segments[0].points[i]
        t.append(temp.time)
        lat.append(temp.latitude)
        lon.append(temp.longitude)
        ele.append(temp.elevation)
        hr.append(int(gpx0.tracks[0].segments[0].points[i].extensions[0][0].text))

    # calculo do tempo com fuso horario
    fuso = timezone(timedelta(hours=-3))
    th = []
    for i in range(0, n, 1):
        th.append(t[i].astimezone(fuso))

    # tempo acumulado em segundos
    dt = [0]
    for i in range(0, n - 1, 1):
        dt.append((t[i + 1] - t[i]).seconds)
    ts = np.cumsum(dt)

    s = [0]
    for i in range(0, n - 1, 1):
        a = (lat[0 + i], lon[0 + i])
        b = (lat[1 + i], lon[1 + i])
        s.append(haversine(a, b) * 1000)  # segmentos

    d = np.cumsum(s)
    delta_ts=np.diff(ts)
    delta_d=np.diff(d)
    delta_d[0]=30
    with np.errstate(divide='ignore', invalid='ignore'):
        pace_total=(delta_ts/60.0)/(delta_d*0.001)
    #identificar pace altos.

    #limpar valores altos e baixos
    id_high=np.where(pace_total>15.0)
    temp_pace = np.delete(pace_total,id_high)
    temp_t = np.delete(delta_ts, [id_high])
    temp_d = np.delete(delta_d, [id_high])

    id_low=np.where(temp_pace< 3.0)
    pacer = np.delete(temp_pace, id_low)
    tsr= np.cumsum(np.delete(temp_t, id_low))
    dr = np.cumsum(np.delete(temp_d, id_low))
    if opt is None:
        pass
    elif (opt.lower())=='print':
        print('Total de pontos excluídos H :',len(id_high[0]))
        print('Total de pontos excluídos L :', len(id_low[0]))
        print('Tamanho vetor               :',len(pacer))
        print('Pace médio                  :',pp_pace(np.mean(pacer)))
        print('Pace max                    :',pp_pace(max(pacer)))
        print('Pace min                    :',pp_pace(min(pacer)))


    return {"t" : tsr, "d" : dr, "p" : pacer}

def gpx_zone_plot(gpxfile,t3km):
    z = vdot3km(t3km)
    out = gpxfile_imp(gpxfile)
    t= out['t']
    d = out['d']
    p= out['p']

    id1 = np.where((p>= z[0][0] / 60) & (p< z[0][1] / 60))
    id2 = np.where((p>= z[1][0] / 60) & (p< z[0][0] / 60))
    id3 = np.where((p>= z[2][0] / 60) & (p< z[1][0] / 60))
    id4 = np.where((p>= z[3][0] / 60) & (p< z[2][0] / 60))
    id5 = np.where((p>= z[4][0] / 60) & (p< z[3][0] / 60))
    id5a = np.where((p>= z[5][0] / 60) & (p< z[4][0] / 60))

    total = len(p)
    z1 = '%05.2f' % (len(id1[0]) / total * 100) + '% '
    z2 = '%05.2f' % (len(id2[0]) / total * 100) + '% '
    z3 = '%05.2f' % (len(id3[0]) / total * 100) + '% '
    z4 = '%05.2f' % (len(id4[0]) / total * 100) + '% '
    z5 = '%05.2f' % (len(id5[0]) / total * 100) + '% '
    z5a = '%05.2f' % (len(id5a[0]) / total * 100) + '% '


    print('Tempo Total de Treino', t[-1])
    tz1  = ts_pace((len(id1[0]) / total )*t[-1])
    tz2  = ts_pace((len(id2[0]) / total )*t[-1])
    tz3  = ts_pace((len(id3[0]) / total )*t[-1])
    tz4  = ts_pace((len(id4[0]) / total )*t[-1])
    tz5  = ts_pace((len(id5[0]) / total )*t[-1])
    tz5a = ts_pace((len(id5a[0]) / total)*t[-1])


    fig, ax = plt.subplots()
    ax.plot(d, p, 'silver', linewidth=2)
    ax.plot(d[id1[0]], p[id1[0]], '.')
    ax.plot(d[id2[0]], p[id2[0]], '.')
    ax.plot(d[id3[0]], p[id3[0]], '.')
    ax.plot(d[id4[0]], p[id4[0]], '.')
    ax.plot(d[id5[0]], p[id5[0]], '.')
    ax.plot(d[id5a[0]], p[id5a[0]], '.')
    ax.legend(['pace médio','Z1-' + z1+ ' ' + tz1,
                            'Z2-' + z2+ ' ' + tz2,
                            'Z3-' + z3+ ' ' + tz3,
                            'Z4-' + z4+ ' ' + tz4,
                            'Z5-' + z5+ ' ' + tz5,
                            'Z6-'+  z5a+' ' +tz5a ])
    ax.set_ylim(ax.get_ylim()[::-1])
    ax.set_xlim(-2, d[-1])
    plt.show()
    return
def find_zones(p,t,d,z):
    """

    :param p: pace
    :param t: time
    :param d: distance
    :param z: zone
    :return:
    """


    id1 = np.where((p >= pace_ts(z[0][1]) / 60) & (p < pace_ts(z[0][0]) / 60))
    id2 = np.where((p >= pace_ts(z[1][1]) / 60) & (p < pace_ts(z[1][0]) / 60))
    id3 = np.where((p >= pace_ts(z[2][1]) / 60) & (p < pace_ts(z[2][0]) / 60))
    id4 = np.where((p >= pace_ts(z[3][1]) / 60) & (p < pace_ts(z[3][0]) / 60))
    id5a = np.where((p >= pace_ts(z[4][1]) / 60) & (p < pace_ts(z[4][0]) / 60))
    id5b = np.where((p >= pace_ts(z[5][1]) / 60) & (p < pace_ts(z[5][0]) / 60))
    id5c = np.where((p >= pace_ts(z[6][1]) / 60) & (p < pace_ts(z[6][0]) / 60))

    total = len(p)
    z1 = '%05.2f' % (len(id1[0]) / total * 100) + '% '
    z2 = '%05.2f' % (len(id2[0]) / total * 100) + '% '
    z3 = '%05.2f' % (len(id3[0]) / total * 100) + '% '
    z4 = '%05.2f' % (len(id4[0]) / total * 100) + '% '
    z5a = '%05.2f' % (len(id5a[0]) / total * 100) + '% '
    z5b = '%05.2f' % (len(id5b[0]) / total * 100) + '% '
    z5c = '%05.2f' % (len(id5c[0]) / total * 100) + '% '

    #print('Tempo Total de Treino', t[-1])
    tz1 = ts_pace((len(id1[0]) / total) * t[-1])
    tz2 = ts_pace((len(id2[0]) / total) * t[-1])
    tz3 = ts_pace((len(id3[0]) / total) * t[-1])
    tz4 = ts_pace((len(id4[0]) / total) * t[-1])
    tz5a = ts_pace((len(id5a[0]) / total) * t[-1])
    tz5b = ts_pace((len(id5b[0]) / total) * t[-1])
    tz5c = ts_pace((len(id5c[0]) / total) * t[-1])

    #total distancia percorridas Zonas



    # resumo
    print('---------------------------------------')
    print('Tempo Total:    ' + ts_pace(t[-1] / 60) + ' min' + '\nVolume. Total:  ' + '%05.2f' % float(d[-1] / 1000) + ' km')
    print('Z1  [' + z[0][0] + '-' + z[0][1] + '] - ' + z1 + '~' + tz1 + 's' + ' ~' + '%05.2f' % (pace_ts(tz1) / 60 * 1 / 5.75) + 'km')
    print('Z2  [' + z[1][0] + '-' + z[1][1] + '] - ' + z2 + '~' + tz2 + 's' + ' ~' + '%05.2f' % (pace_ts(tz2) / 60 * 1 / 5.00) + 'km')
    print('Z3  [' + z[2][0] + '-' + z[2][1] + '] - ' + z3 + '~' + tz3 + 's' + ' ~' + '%05.2f' % (pace_ts(tz3) / 60 * 1 / 4.50) + 'km')
    print('Z4  [' + z[3][0] + '-' + z[3][1] + '] - ' + z4 + '~' + tz4 + 's' + ' ~' + '%05.2f' % (pace_ts(tz4) / 60 * 1 / 4.25) + 'km')
    print('Z5a [' + z[4][0] + '-' + z[4][1] + '] - ' + z5a + '~' + tz5a + 's' + ' ~' + '%05.2f' % (pace_ts(tz5a) / 60 * 1 / 4.06) + 'km')
    print('Z5b [' + z[5][0] + '-' + z[5][1] + '] - ' + z5b + '~' + tz5b + 's' + ' ~' + '%05.2f' % (pace_ts(tz5b) / 60 * 1 / 3.83) + 'km')
    print('Z5c [' + z[6][0] + '-' + z[6][1] + '] - ' + z5c + '~' + tz5c + 's' + ' ~' + '%05.2f' % (pace_ts(tz5c) / 60 * 1 / 3.58) + 'km')



    fig, ax = plt.subplots()
    ax.plot(d, p, 'silver', linewidth=2)
    ax.plot(d[id1[0]], p[id1[0]], '.')
    ax.plot(d[id2[0]], p[id2[0]], '.')
    ax.plot(d[id3[0]], p[id3[0]], '.')
    ax.plot(d[id4[0]], p[id4[0]], '.')
    ax.plot(d[id5a[0]], p[id5a[0]], '.')
    ax.plot(d[id5b[0]], p[id5b[0]], '.')
    ax.plot(d[id5c[0]], p[id5c[0]], '.')
    ax.set_title('Tempo Total: ' + ts_pace(t[-1]/60) + ' min'+ '\n Vol. Total: '+'%05.2f' %float(d[-1]/1000)+'km')
    ax.set_ylim(ax.get_ylim()[::-1])
    #
    ax.legend(['Pace',
                'Z1  ( ' + z[0][0] + '-' + z[0][1] + ') - ' + z1 + 'Tempo ' + tz1 + 's' ,
                'Z2  ( ' + z[1][0] + '-' + z[1][1] + ') - ' + z2 + 'Tempo ' + tz2 + 's' ,
                'Z3  ( ' + z[2][0] + '-' + z[2][1] + ') - ' + z3 + 'Tempo ' + tz3 + 's' ,
                'Z4  ( ' + z[3][0] + '-' + z[3][1] + ') - ' + z4 + 'Tempo ' + tz4 + 's' ,
                'Z5a ( ' + z[4][0] + '-' + z[4][1] + ') - ' + z5a + 'Tempo ' + tz5a + 's',
                'Z5b ( ' + z[5][0] + '-' + z[5][1] + ') - ' + z5b + 'Tempo ' + tz5b + 's',
                'Z5c ( ' + z[6][0] + '-' + z[6][1] + ') - ' + z5c + 'Tempo ' + tz5c + 's'])
    ax.set_ylim(ax.get_ylim()[::-1])
    ax.set_ylim(8,3)
    ax.set_xlim(-2, d[-1])
    plt.show()


def gpx_zone_plot2(filegpx,ftpa):
    """

    :param filegpx: file gpx
    :param ftpa: Functional Threshold Pace (FTPa) ~ pace limiar.  Run for 30 minutes at a strong but steady pace. Calculate the average pace
    during this period.
    :return:
    """

    z = pace_zones(ftpa)
    out = gpxfile_imp(filegpx)
    t= out['t']
    d = out['d']
    p= out['p']

    #identificando as zonas nos dados
    find_zones(p,t,d,z)

    return
def plot_zones():
    z=pace_zones('4:10')
    print(z[0][0],z[0][1])
    print(z[1][0], z[1][1])
    print(z[2][0], z[2][1])
    print(z[3][0], z[3][1])

    fig, ax = plt.subplots()
    t=np.linspace(0,15,120)
    y=1.25*np.sin(t/2)*np.cos(t*2)+4.8
    ax.plot(t,y,color=(1,1,1,1))
    ax.axhspan(pace_ts(z[0][0])/60, pace_ts(z[0][1])/60, color=(0.0, 0.0, 0.25),  alpha=0.5)
    ax.axhspan(pace_ts(z[1][0])/60, pace_ts(z[1][1])/60, color=(0.1, 0.2, 0.25),  alpha=0.5)
    ax.axhspan(pace_ts(z[2][0])/60, pace_ts(z[2][1])/60, color=(0.2, 0.3, 0.25),  alpha=0.5)
    ax.axhspan(pace_ts(z[3][0])/60, pace_ts(z[3][1])/60, color=(0.3, 0.4, 0.25),  alpha=0.6)
    ax.axhspan(pace_ts(z[4][0])/60, pace_ts(z[4][1])/60, color=(0.4, 0.3, 0.25),  alpha=0.6)
    ax.axhspan(pace_ts(z[5][0])/60, pace_ts(z[5][1])/60, color=(0.6, 0.2, 0.25),  alpha=0.6)
    ax.axhspan(pace_ts(z[6][0])/60, pace_ts(z[6][1])/60, color=(0.7, 0.0, 0.25),  alpha=0.6)
    ax.set(ylim=(pace_ts(z[6][1])/60, pace_ts(z[0][0])/60), title="axhspan")
    #ax.set_ylim(ax.get_ylim()[::-1])

    plt.show()

def vol_zone(path_files):
    """
    calcule total volumes in the week or month e total for each training zone
    :return:
    """
    #Read files from the directory and select only GPX files.
    z = pace_zones('4:08')
    gpx_files=gpx_dir(path_files)
    #gpx_files = []
    # try:
    #     dir_list = os.listdir(path_files)
    #     for file in dir_list:
    #         if file.endswith(".gpx"):
    #             gpx_files.append(file)
    #     if len(gpx_files)==0:
    #         print('Não há arquivos GPX')
    #         return []
    # except FileNotFoundError:
    #     print(f"ERRO: O diretório '{path_files}' não foi encontrado.")
    #     return []

    s=0
    s_total=0
    t_total=0
    count_file=0
    d_sum=[]
    t_sum=[]
    p_sum=[]
    for file in gpx_files:
        out=gpxfile_imp(path_files+'/'+file)
        d=out['d']
        t=out['t']
        p=out['p']
        if count_file==0:
            d_sum=d
            t_sum=t
            p_sum=p

        #print(file,d[-1]/1000,len(d),)
        s_total+=d[-1]
        t_total+=t[-1]
        s+=len(d)
        count_file+=1
        if count_file > 1:
            d_end=d_sum[-1]
            t_end=t_sum[-1]
            for i in range(len(d)):
                d_sum = np.append(d_sum, d_end + d[i])
                t_sum = np.append(t_sum, t_end + t[i])
                p_sum = np.append(p_sum, p[i])


    # print(' --------------------')
    # print('numero de pontos',s)
    # print('distancia total',s_total/1000,'km')
    # print('tempo total',pp_pace(t_total/3600) , 'min')
    # print(len(d_sum),d_sum[-1])
    # print(len(t_sum),t_sum[-1]/3600)
    # print(len(p_sum))

    p=p_sum
    d=d_sum
    t=t_sum

    find_zones(p,t,d,z)