# 원래 하던것 처럼 Deep Learning Model의 Input을 불러오는 파일
# Input은 idx으로 이는 실험 결과의 ap_idx가 인자로 받아들어옴
# return img_input(img test), num_input(numeric_test)
import glob
import numpy as np
import pandas as pd
import math
import utm
from math import pi


def load_input(pci,azi,down):
    rss_path = 'C:\\GBAG_WEB\\gbag\\static\\csv\\maps\\RSS_realmatched.csv'
    jangbi_path = 'C:\\GBAG_WEB\\gbag\\static\\csv\\maps\\jangbi.csv'
    rss = pd.read_csv(rss_path)
    pci_point = pd.read_csv(jangbi_path, encoding='cp949')

    # 안테나의 위치
    tx=pci_point['Longitude'][int(pci)-1]
    ty=pci_point['Latitude'][int(pci)-1]
    tz=pci_point['Height (m)'][int(pci)-1]

    # LAMS 이미지 5x5
    lams_path='C:\\GBAG_WEB\\gbag\\static\\lams\\pci'+pci+'_grid_20_20_100_v1'
    print('램스경로: '+lams_path)
    img_data = []
    for file in glob.glob(lams_path+'/*.npy'):
        img_data.append(np.load(file))
    img_test = np.array(img_data)

    numeric_data_test = pd.read_csv('C:\\GBAG_WEB\\gbag\\static\\csv\\test\\grid_5.csv')    # 좌표 파일 읽기

    chai_list = []
    chai2_list = []
    dist_list =[]

    # RX 좌표 변환 + chai1 계산 + chai2 계산
    for i in range(len(numeric_data_test)):
        
        azi = int(azi)
        dt = int(down)
        rx = numeric_data_test.RX[i]
        ry = numeric_data_test.RY[i]
        rz = numeric_data_test.RZ[i]
        
        new_rx=rx-tx
        new_ry=ry-ty
        new_rz=rz-tz
        
        temp_azi = math.atan2(new_ry,new_rx) #rx 각도 구하기 atan2로
        temp2_azi = temp_azi * 180 / pi #라디안을 각도로 변환

        if temp2_azi < 0:         
            temp2_azi = 360 + temp2_azi

        if 0<=azi<=90:
            azi = 90 - azi

        else:
            azi = 360 - (azi - 90)

        n_azi=math.radians(azi) #라디안을 각도로 변환
        chai1=abs(azi-temp2_azi)
        if chai1>180:
            chai1=360-chai1
        chai_list.append(chai1)
        
        temp_dt = math.atan2(new_rz,new_ry) #rx 각도 구하기 atan2로, x축으로 바꾸려면 new_ry를 new_rx로
        temp2_dt = temp_dt * 180 / pi #라디안을 각도로 변환

        if temp2_dt < 0:         
            temp2_dt = temp2_dt*(-1)
        else:
            temp2_dt=360-temp2_dt

        chai2=abs(temp2_dt-dt)
        
        if chai2>180:
            chai2=360-chai2
        chai2_list.append(chai2)
        
        dist_list=math.sqrt(((tx-rx) * (tx-rx) ) + ((ty-ry)  * (ty-ry))+((tz-rz) * (tz-rz)))

    numeric_data_test["chai1"]=chai_list
    numeric_data_test["chai2"]=chai2_list
    numeric_data_test["dist"]=dist_list

    x_test = np.zeros((len(numeric_data_test), 3))
    
    for j in range(len(numeric_data_test)):
        x_test[j][0] = numeric_data_test['chai1'][j] / 179.9734786654863  # azimuth 최댓값으로 나눔
        x_test[j][1] = numeric_data_test['chai2'][j] / 180.0   # downtilt 최댓값으로 나눔
        x_test[j][2] = numeric_data_test['dist'][j] / 361.0   # distance 최댓값으로 나눔
    
    numeric_test = np.array(x_test)

    return img_test, numeric_test
    