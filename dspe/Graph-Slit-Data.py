import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import csv

pol_list = [0,30,60,70,75,80,85,90]

Rquantdict = {
    0 : csv.DictReader(open('dspe/physdata/quant0.csv', 'r')),
    30: csv.DictReader(open('dspe/physdata/quant30.csv', 'r')),
    60: csv.DictReader(open('dspe/physdata/quant60.csv', 'r')),
    70: csv.DictReader(open('dspe/physdata/quant70.csv', 'r')),
    75: csv.DictReader(open('dspe/physdata/quant75.csv', 'r')),
    80: csv.DictReader(open('dspe/physdata/quant80.csv', 'r')),
    85: csv.DictReader(open('dspe/physdata/quant85.csv', 'r')),
    90: csv.DictReader(open('dspe/physdata/quant90.csv', 'r'))
}

quant_dict = {
    0:{"I":[], "Angle":[]},
    30:{"I":[], "Angle":[]},
    60:{"I":[], "Angle":[]},
    70:{"I":[], "Angle":[]},
    75:{"I":[], "Angle":[]},
    80:{"I":[], "Angle":[]},
    85:{"I":[], "Angle":[]},
    90:{"I":[], "Angle":[]}
}

I_list = []
angle_list = []
for angle in pol_list:
    for entry in Rquantdict[angle]:
        I_list.append(float(entry["Irel (mA)"]))
        angle_list.append(float(entry["Angle (Ëš)"]))
    quant_dict[angle]["I"] = I_list
    quant_dict[angle]["Angle"] = angle_list
    I_list = []
    angle_list = []
    
Rqualdict = {
    0 : csv.DictReader(open('dspe/physdata/qualitative0.csv', 'r')),
    30: csv.DictReader(open('dspe/physdata/qualitative30.csv', 'r')),
    60: csv.DictReader(open('dspe/physdata/qualitative60.csv', 'r')),
    70: csv.DictReader(open('dspe/physdata/qualitative70.csv', 'r')),
    75: csv.DictReader(open('dspe/physdata/qualitative75.csv', 'r')),
    80: csv.DictReader(open('dspe/physdata/qualitative80.csv', 'r')),
    85: csv.DictReader(open('dspe/physdata/qualitative85.csv', 'r')),
    90: csv.DictReader(open('dspe/physdata/qualitative90.csv', 'r'))
}

qual_dict = {
    0:{"I":[], "Time":[]},
    30:{"I":[], "Time":[]},
    60:{"I":[], "Time":[]},
    70:{"I":[], "Time":[]},
    75:{"I":[], "Time":[]},
    80:{"I":[], "Time":[]},
    85:{"I":[], "Time":[]},
    90:{"I":[], "Time":[]}
}

I_list = []
time_list = []
for angle in pol_list:
    for entry in Rqualdict[angle]:
        I_list.append(float(entry['Current']))
        time_list.append(float(entry['Time']))
    qual_dict[angle]["I"] = I_list
    qual_dict[angle]["Time"] = time_list
    I_list = []
    time_list = []

RqualBlocked = csv.DictReader(open('dspe/physdata/qualitative-blocked-slit.csv', 'r')),
qual_blocked = {"I":[], "Time":[]}
for entry in RqualBlocked[0]:
    I_list.append(float(entry['Current']))
    time_list.append(float(entry['Time']))
qual_blocked["I"] = I_list
qual_blocked["Time"] = time_list

plt.figure(1)
plt.plot(
    quant_dict[0]["Angle"], quant_dict[0]["I"], 'ro',
    quant_dict[30]["Angle"], quant_dict[30]["I"], 'go',
    quant_dict[60]["Angle"], quant_dict[60]["I"], 'bo',
    quant_dict[70]["Angle"], quant_dict[70]["I"], 'co',
)

plt.figure(2)
plt.plot(
    qual_blocked["Time"], qual_blocked["I"], 'r-'
)

dlratio = 198/28.5

def beta(theta):
    return 2*math.pi*dlratio*math.sin(theta)

alratio = 40/28.5

def alpha(theta):
    return math.pi*alratio*math.sin(theta)

def PolarisedInt(theta, p):
    return (math.sin(alpha(theta))/alpha(theta))**2*(1+math.cos(p)**4+2*math.cos(p)**2*math.cos(beta(theta)))
vectPolInt = np.vectorize(PolarisedInt)

X, Y = np.meshgrid(np.linspace(-math.pi/2, math.pi/2, 2280), np.linspace(0, math.pi/2, 2280))
Z = vectPolInt(X, Y)

plt.figure(3)
plt.pcolormesh(X, Y, Z, vmax=1.2, cmap='plasma')

plt.show()

