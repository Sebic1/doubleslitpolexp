import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import pandas as pd
import csv
from cycler import cycler

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
        angle_list.append(float(entry["Angle (˚)"]))
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

#plt.figure(1)
#plt.plot(
#    quant_dict[0]["Angle"], quant_dict[0]["I"], 'ro',
#    quant_dict[30]["Angle"], quant_dict[30]["I"], 'go',
#    quant_dict[60]["Angle"], quant_dict[60]["I"], 'bo',
#    quant_dict[70]["Angle"], quant_dict[70]["I"], 'co',
#)
#
plt.figure(2)
plt.plot(
    qual_blocked["Time"], qual_blocked["I"], 'r-',
)
plt.xlabel('Time (s)')
plt.ylabel('Relative Intensity (mA)')
plt.title('Qualitative Data for Blocked Slit, Double Slit Light Intensity')

plt.figure(1)
plt.plot(
    qual_dict[90]["Time"], qual_dict[90]["I"], 'r-'
)

dlratio = 198/28.5

def beta(theta):
    return 2*math.pi*dlratio*math.sin(theta)

alratio = 40/28.5

def alpha(theta):
    return math.pi*alratio*math.sin(theta)

def sinc(x):
    if x == 0:
        return 1
    else:
        return math.sin(x)/x

def PolarisedInt(theta, p):
    return (sinc(alpha(theta)))**2*(1+math.cos(p)**4+2*math.cos(p)**2*math.cos(beta(theta)))
vectPolInt = np.vectorize(PolarisedInt)

X, Y = np.meshgrid(np.linspace(-90, 90, 2280), np.linspace(0, 90, 2280))
Z = vectPolInt(X*math.pi/180, Y*math.pi/180)

plt.figure(3)
plt.suptitle('Polarised Slit, Double Slit Light Relative Intensity Theoretical')
plt.subplot(1, 2, 1)
plt.pcolormesh(X, Y, Z, cmap='GnBu_r', norm=mpl.colors.LogNorm(vmin=Z.min(), vmax=Z.max()))
plt.colorbar()
plt.title('Logarithmic')
plt.xlabel('Angle From Center (˚)')
plt.ylabel('Angle of Polariser from Normal (˚)')

plt.subplot(1, 2, 2)
plt.pcolormesh(X, Y, Z, cmap='plasma')
plt.colorbar()
plt.title('Normal')
plt.xlabel('Angle From Center (˚)')
plt.ylabel('Angle of Polariser from Normal (˚)')

X = np.linspace(0,90,1000)
pol_angle = 90
Y = vectPolInt(X*math.pi/180, pol_angle*math.pi/180)*quant_dict[pol_angle]["I"][0]*1

rad_list = []
for angle in quant_dict[pol_angle]["Angle"]:
    rad_list.append((180 - angle))

plt.figure(4)
plt.plot(
    rad_list, quant_dict[pol_angle]["I"], 'ro',
    label = "Quantatative Data"
)
plt.plot(
    X, Y, 'b-',
    label = "Theoretical Data"
)

plt.xlabel('Measurement Angle from Center (˚)')
plt.ylabel('Relative Intensity (mA)')
plt.title(f'{pol_angle}˚ Polarised Slit, Double Slit Light Intensity')
plt.legend()

plt.figure(5)

X = np.linspace(0,1,15000)

Y = {}
select_pol_list = [30,70,80,85,90]
for angle in select_pol_list:
    frac = len(qual_dict[angle]["I"])/X.size
    newY = []
    index = 0
    for n in np.nditer(X):
        newY.append(qual_dict[angle]["I"][math.floor(index)])
        index += frac
    Y[angle] = newY
    
cmap = mpl.colormaps['plasma']
colours = cmap(np.linspace(0,1,len(select_pol_list)))
    
i = 0
for angle, plot in Y.items():
    plt.plot(
        X, plot,
        label = f'{angle}˚',
        color = colours[i]
    )
    i += 1
    
plt.xlabel('Scaled Time Measurement')
plt.ylabel('Relative Intensity (mA)')
plt.title('Qualitative Data for Polarised Slit, Double Slit Light Intensity')
plt.legend()

plt.show()

