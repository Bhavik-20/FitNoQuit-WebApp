import pandas as pd
import numpy as np
import math
from sklearn.metrics import mean_squared_error

df = pd.read_csv('wo_data.csv')

wt1 = []
wt2 = []
wt3 = []
wt4 = []
for i in range(0, len(df['130 lb'])):
    wt1.append(130)
    wt2.append(155)
    wt3.append(180)
    wt4.append(205)
df['weight1'] = wt1
df['weight2'] = wt2
df['weight3'] = wt3
df['weight4'] = wt4

c = []
for i in range(0,len(df['130 lb'])):
    cf = 0
    c1 = df.loc[i][1] - (df['CPK'][i] * 60) 
    c2 = df.loc[i][2] - (df['CPK'][i] * 70) 
    c3 = df.loc[i][3] - (df['CPK'][i] * 82) 
    c4 = df.loc[i][4] - (df['CPK'][i] * 93)
    cf = (c1+c2+c3+c4)/4
    c.append(cf)
c = sum(c) / len(c)

#################### Take from Database ##########################
calories = 200 
#################### Take from Database ##########################

time = [0.5, 0.75, 1] #30 mins, 45 mins, 1hr
w = 70
l = []
for i in range(0, len(df)):
    # cpk = df['CPK'][i] * w
    cpk = df['CPK'][i]*w + c 
    for t in time:
        if cpk * t <= 220 and cpk * t >= 180:
            l.append((df['Activity, Exercise or Sport (1 hour)'][i], t, math.ceil(cpk * t)))
print(l)