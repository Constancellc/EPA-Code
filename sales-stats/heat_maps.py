import csv
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import random
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

blues = cm.get_cmap('Oranges', 1000)
new = blues(np.linspace(0, 1, 1000))
new[:1,:] =  np.array([1,1,1,1])
blue2 = ListedColormap(new)

lsoa2la = {}
gas = '../../Documents/elec_demand/LSOA_domestic_electricity_2017.csv'
flats = {}
houses = {}

with open(gas,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for i in range(0):
        next(reader)
    for row in reader:
        lsoa2la[row[5]] = row[1]
        
stem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'
dwell = '../../Documents/census/dwellingType-LSOA.csv'


with open(dwell,'rU') as csvfile:
    reader = csv.reader(csvfile)
    for i in range(10):
        next(reader)
    for row in reader:
        if len(row) < 9:
            continue
        try:
            la = lsoa2la[row[0][:9]]
        except:
            print(row)
            continue
        if la not in flats:
            flats[la] = 0
            houses[la] = 0

        houses[la] += int(row[3])+int(row[4])+int(row[5])
        flats[la] += int(row[7])+int(row[8])+int(row[6])

data = {}
for la in flats:
    try:
        data[la] = [(flats[la]*0.25+houses[la]*0.04)/(flats[la]+houses[la]),
                    (flats[la]+houses[la]*0.16)/(flats[la]+houses[la]),
                    0.999]
                    
    except:
        continue
    
locs = {}
with open(stem+'LA-lat-lon.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[1]] = [float(row[3]),float(row[2])]

years = [2020,2025,2030]

def scurve(data,x):
    _x = [2017,2030,2050]
    y = []
    for i in range(3):
        y.append(np.log(data[i]/(1-data[i])))
    [m,c] = np.polyfit(_x,y,1)

    f = []
    for i in range(len(x)):
        f.append(1/(1+np.exp(-1*(m*x[i]+c))))
    return f


pList = []
z = []
z2 = []
z3 = []

lalist = []

for p in data:
    try:
        pList.append(locs[p])
        lalist.append(p)
    except:
        continue

    f = scurve(data[p],years)
    z.append(100*f[0])
    z2.append(100*f[1])
    z3.append(100*f[2])



fig=plt.figure(figsize=(10,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 12

plt.subplot(1,3,1)
plt.title(str(years[0]))
ax = plt.gca()
# setup mercator map projection.


m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=58.7,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)


def find_nearest(p1):
    closest = 100000
    best = None

    for ii in range(len(pList)):
        p = pList[ii]
        d = np.power(p[0]-p1[1],2)+np.power(p[1]-p1[0],2)
        if d < closest:
            closest = d
            best = ii

    return best

x = np.arange(-7,3,0.2)
y = np.arange(49,59,0.2)

Z = np.zeros((len(x),len(y)))
Z2 = np.zeros((len(x),len(y)))
Z3 = np.zeros((len(x),len(y)))
X = np.zeros((len(x),len(y)))
Y = np.zeros((len(x),len(y)))
m.drawcoastlines()
for i in range(len(x)):
    for j in range(len(y)):
        p = [x[i],y[j]]
        best = find_nearest(p)
        xpt,ypt = m(x[i],y[j])
        X[i,j] = xpt
        Y[i,j] = ypt
        if m.is_land(xpt,ypt) == True:
            if xpt < 200000 and ypt < 970000 and ypt > 300000:
                continue
            if xpt > 885000 and ypt < 175000:
                continue
            if xpt > 766000 and ypt < 104000:
                continue
            Z[i,j] = z[best]
            Z2[i,j] = z2[best]
            Z3[i,j] = z3[best]
        else:
            continue
        
im = m.pcolor(X,Y,Z,vmin=0,vmax=100,cmap=blue2)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)

plt.subplot(1,3,2)
plt.title(str(years[1]))
ax = plt.gca()
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=58.7,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)
m.drawcoastlines()
im = m.pcolor(X,Y,Z2,vmin=0,vmax=100,cmap=blue2)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)

plt.subplot(1,3,3)
plt.title(str(years[2]))

ax = plt.gca()
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=58.7,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)
            
m.drawcoastlines()
im = m.pcolor(X,Y,Z3,vmin=0,vmax=100,cmap=blue2)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)

plt.tight_layout()
#plt.savefig('../../Dropbox/thesis/chapter3/img/scurve.eps', format='eps', dpi=1000,
#            bbox_inches='tight', pad_inches=0)
plt.savefig('../../Dropbox/papers/proposal/eh_scurve.eps', format='eps', dpi=300,
            bbox_inches='tight', pad_inches=0)


plt.show()
        

