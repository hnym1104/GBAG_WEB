import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import math
from math import pi
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches as patches


def visualize_result(pci,azi,down,predictions):
    building_path = 'C:\GBAG_WEB\\gbag\static\\building\\Cropped.shp'
    jangbi_path = 'C:\GBAG_WEB\\gbag\\static\\csv\\maps\\jangbi.csv'
    building = gpd.read_file(building_path)
    jangbi = pd.read_csv(jangbi_path, encoding='cp949')
    plt.rcParams["figure.figsize"] = (8, 6) # 그림 크기 설정

    numeric_data_test = pd.read_csv('C:\GBAG_WEB\\gbag\\static\\csv\\test\\grid_5.csv')    # 파일 읽기

    ### prediction min, max 확인
    predictions_min = np.min(predictions)
    predictions_max = np.max(predictions)
        
    numeric_data_test["RSRP"]=predictions


    # Plot 설정
    fig, ax = plt.subplots(1, 1) # plot과 legend 띄우기
    ax.set_xlim([325879, 326290])
    ax.set_ylim([4151000,4151315])
    divider = make_axes_locatable(ax) # legend 분리
    cax = divider.append_axes("right", size="2%", pad=0.1) # legend 사이즈 조정

    # Rx Plot
    RX_coord = gpd.points_from_xy(numeric_data_test.RX,numeric_data_test.RY) # Rx 좌표->points로 변환
    RX_gdf = gpd.GeoDataFrame(numeric_data_test.RSRP, geometry = RX_coord, crs=32652) # RSRP값과 좌표를 geodataframe으로 변환 (좌표계: 32652)
    RX_gdf.plot(column=numeric_data_test.RSRP, legend=True, ax=ax, cax=cax, s=50, marker='s', 
                vmin=predictions_min, vmax=predictions_max, cmap='jet') # Rx값 Plot (색=RSRP)

    #arrow 각도 계산
    azimuth2 = int(azi)
    if 0<=azimuth2<=90:
        azimuth2 = 90 - azimuth2

    else:
        azimuth2 = 360 - (azimuth2 - 90)
    
    radi_azi = azimuth2 * pi / 180

    # Tx Plot
    TX_coord = gpd.points_from_xy(jangbi.Longitude, jangbi.Latitude) # Tx 좌표->points로 변환
    TX_gdf = gpd.GeoDataFrame(jangbi['idx'], geometry = TX_coord, crs=32652) # PCI값과 좌표를 geodataframe으로 변환 (좌표계: 32652)

    ax.add_patch(
    patches.Arrow(
        TX_coord[int(pci)-1].x, TX_coord[int(pci)-1].y,
        16*math.cos(radi_azi), 16*math.sin(radi_azi),
        width = 15, linewidth=2, edgecolor = '#FF1493',
        facecolor = '#FFFFFF'
    ))
    

    
    # 건물 Plot
    building.plot(column="AGL", cmap='gist_gray', ax=ax) # 빌딩 플롯 (색=AGL)
    

    ### 이미지 저장 코드
    fig.savefig('C:\GBAG_WEB\\gbag\\static\\img\\result_image.png', dpi=250)