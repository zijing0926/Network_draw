# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:16:19 2019

@author: zzhu1
"""

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
from mpl_toolkits.basemap import Basemap
import os

os.environ['PROJ_LIB'] = r'C:\Users\zzhu1\Anaconda3\Library\share'

from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import geopandas as gpd
import descartes
from shapely.geometry import Point,Polygon
#import cv2

#from mpl_toolkits.basemap import Basemap as Basemap

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']


city_sta1=pd.read_excel('coor.xlsx')
additional=pd.read_excel('additional.xlsx')
lis=[city_sta1,additional]
city_sta=pd.concat(lis,sort=False)
city_sta=city_sta.drop_duplicates(subset='city_cn',keep='first')
#city_sta=city_sta[city_sta['level']=='city']
city_sta=city_sta.drop(['level'],axis=1)
#sta=pd.read_excel('station.xlsx')
#sta.drop(sta.columns[[0, 1 ]], axis = 1, inplace = True)
#city_sta=sta.drop_duplicates(subset='city', keep='first')
#city_sta['city'] = (city_sta['city']+'市')
variables=pd.read_excel('variables.xlsx')
#get rid of the provinces
variables=variables[~variables['city_cn'].str.contains('省')]
variables=variables[~variables['city_cn'].str.contains('自治区')]
variables['employment']=variables['employ1']+variables['employ2']
variables=variables[['city_cn', 'Population','year','employment','gdp']]
variables=variables.sort_values(by=['city_cn','year'])
variables=variables.fillna(method='ffill')
variables2017=variables[variables['year']==2017]
variables2017['year']=2018
frames=[variables,variables2017]
variables=pd.concat(frames)

all_dfs = pd.read_excel('network.xlsx', sheet_name=None,header=None,names=['city_from','city_to','net','year'])
df = pd.concat(all_dfs, ignore_index=True)
year_lis=[2012,2013]
#variables=variables[~variables['city_cn'].str.contains('巢湖市')]

year=2008
for year in range(2008,2019):
    df_copy=df
    df1=df_copy[df_copy['year']==year]
    df1=df1.merge(city_sta,left_on='city_from',right_on='city_cn',how='left')
    df1=df1.merge(city_sta,left_on='city_to',right_on='city_cn',how='left')
    city=df1['city_from'].unique().tolist()
    city1=df1['city_to'].unique().tolist()
    for c in city1:
        city.append(c)
    city_list=pd.DataFrame(city)
    city_list=city_list.drop_duplicates(keep='first')
    city_list.columns=['city_cn']
    
    #df1=df1.dropna()
    city_sta_copy=city_sta
    city_sta_copy=city_sta_copy.merge(city_list,on='city_cn',how='right')
    variables_copy=variables[variables['year']==year]
    variables_copy=variables_copy.drop_duplicates(subset='city_cn',keep='first')
    city_sta_c=city_sta_copy.merge(variables_copy,on='city_cn',how='left')
    city_sta_c['year'].fillna(year, inplace = True) 
    city_sta_c=city_sta_c.fillna(value=1)
    graph = nx.from_pandas_edgelist(df1, source = 'city_from', target = 'city_to')
    m= Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, \
          projection='lcc', lat_1=33, lat_2=45, lon_0=100) 

    #m.readshapefile(r'C:\Users\zzhu1\Documents\hsr\gadm36_CHN_1', 'states', drawbounds = True)
    mx, my = m(city_sta['lon'].values, city_sta['lat'].values)
    pos = {}
    for count, elem in enumerate (city_sta['city_cn']):
        pos[elem] = (mx[count], my[count])
    plt.figure(figsize=(8,8))
    #if year==2008:
     #   nx.draw_networkx(graph, pos,with_labels=False,
      #               node_size = [city_sta_c.loc[city_sta_c['city'] == s, 'employment'].item()*0.001 for s in graph.nodes()])
        
    #elif year in year_lis:
     #   nx.draw_networkx(graph, pos,with_labels=False,
      #               node_size = [city_sta_c.loc[city_sta_c['city'] == s, 'employment'].item()*0.1 for s in graph.nodes()])
    #elif year==2018:
     #   nx.draw_networkx(graph, pos,with_labels=False,node_size=50)
        
    #else:
    nx.draw_networkx(graph, pos=pos,with_labels=False,alpha=0.5,
                     node_size = [city_sta_c.loc[city_sta_c['city_cn'] == s, 'employment'].item() for s in graph.nodes()])
    nx.draw_networkx_labels(graph, pos, labels={'北京市': 'Beijing', '上海市': 'Shanghai', '广州市': 'Guangzhou', '成都市': 'Chengdu','武汉市': 'Wuhan'}, font_size=15, font_color='r')    
    m.drawcountries(linewidth = 3)
    m.drawstates(linewidth = 0.2)
    m.drawcoastlines(linewidth=3)
    plt.tight_layout()
    plt.title('HSR Network in %d'%year)
    plt.savefig('hsr_%d'%year)
    year=year+1




import matplotlib.animation as animation
import matplotlib.image as mpimg 
fig = plt.figure()
ims=[]
for i in range(2008,2019):
    img = mpimg.imread('hsr_%d.png'%i) 
    im=plt.imshow(img,animated=True)
    ims.append([im])


fig = plt.figure()
ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)

ani.save('dynamic_images.gif')

plt.show()
import os
from PIL import Image
path = os.getcwd()
files = os.listdir(path)
figure_hsr=[f for f in files if f[:5]=='hsr_2']
images = []
for file in figure_hsr:
    img = Image.open(file)
    images.append(img)
ims=[]
im=plt.imshow(images[0],animated=True)
ims.append([im])
im=plt.imshow(images[1],animated=True)
ims.append([im])
