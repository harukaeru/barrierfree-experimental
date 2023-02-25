import pandas as pd
from geopy.distance import geodesic
import networkx as nx
import numpy as np
import math
from math import radians, cos, sin, asin, sqrt

df = pd.read_csv('mlit_housing_nintei.csv', encoding='cp932')

df['name'] = df['name'].str.strip()
df.replace({'latitude': {'-': pd.np.nan}, 'longitude': {'-': pd.np.nan}}, inplace=True)
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 小数点以下6桁で緯度・経度を取得しているため、ラジアンに変換する
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # メルカトル図法に基づく座標変換
    k = 2 * asin(sqrt(sin((lat1 - lat2) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon1 - lon2) / 2) ** 2))
    r = 6371  # 地球の半径（km）
    return k * r

df.dropna(subset=['latitude', 'longitude'], inplace=True)

# print(df.head())

coords = list(zip(df['latitude'], df['longitude']))

def norm(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return math.sqrt(x * x + y * y)

# print('length', len(coords))
# 地点間の距離を計算する
distances = []
for i in range(len(coords)):
    row = []
    for j in range(len(coords)):
        if i == j:
            row.append(0)
        else:
            d = haversine(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
            row.append(d)
    distances.append(row)

# print(distances)

# 距離行列からグラフを作成する
G = nx.Graph()
for i in range(len(distances)):
    for j in range(i+1, len(distances)):
        G.add_edge(i, j, weight=distances[i][j])

# print(G)

# 最小全域木を求める
T = nx.minimum_spanning_tree(G)

# 最小全域木のエッジを表示する
print('Source,Target,Weight')
for u, v, d in T.edges(data=True):
    # print(f"{df.iloc[u]['name']},{df.iloc[u]['add.']},{df.iloc[v]['name']},{df.iloc[v]['add.']},{d['weight']}")
    print(f"{df.iloc[u]['name']},{df.iloc[v]['name']},{d['weight']}")
