import csv
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import random
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

blues = cm.get_cmap('Blues', 1000)
new = blues(np.linspace(0, 1, 1000))
new[:1,:] =  np.array([1,1,1,1])
blue2 = ListedColormap(new)
'''
fig=plt.figure(figsize=(9,2.7))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 11

def ff(x,a,b):
    y = []
    for i in range(len(x)):
        y.append(1/(1+a*np.exp(-b*x[i])))
    return y

_a = [10,100]
_b = [10,100]

plt.subplot(1,3,1)
plt.plot(np.arange(0,100,0.1),ff(np.arange(0,100,0.1),100,0.2))
plt.grid()
plt.ylim(0,1)
plt.xlim(0,99)
plt.yticks(np.arange(0,1.2,0.2),['0','20','40','60','80','100'])
plt.xlabel('Time (years)')
plt.ylabel('Penetration (%)')
plt.title(r'$\alpha=100,\beta=0.2$')
#plt.title(r'$\alpha = 100\n$\beta = 0.2')
plt.subplot(1,3,2)
plt.title(r'$\alpha=100,\beta=0.1$')
plt.yticks(np.arange(0,1.2,0.2),['']*6)
plt.plot(np.arange(0,100,0.1),ff(np.arange(0,100,0.1),100,0.1))
plt.grid()
plt.ylim(0,1)
plt.xlim(0,99)
plt.xlabel('Time (years)')
plt.subplot(1,3,3)
plt.title(r'$\alpha=1000,\beta=0.1$')
plt.plot(np.arange(0,100,0.1),ff(np.arange(0,100,0.1),1000,0.1))
plt.yticks(np.arange(0,1.2,0.2),['']*6)
plt.grid()
plt.ylim(0,1)
plt.xlim(0,99)
plt.tight_layout()
plt.xlabel('Time (years)')
plt.savefig('../../Dropbox/thesis/chapter3/img/scurve_egs.eps', format='eps', dpi=1000,
            bbox_inches='tight', pad_inches=0)
plt.show()


'''
total = {}
_2017 = {}
_2018 = {}
name = {}
data = {}

years = [2020,2025,2030]

stem = '../../Documents/simulation_results/NTS/clustering/power/locationsLA_/'

def scurve(data,x):
    _x = np.arange(2011.75,2018.75,0.25)
    y = []
    for i in range(len(data)):
        y.append(np.log(data[i]/(1-data[i])))
    [m,c] = np.polyfit(_x,y,1)

    f = []
    for i in range(len(x)):
        f.append(1/(1+np.exp(-1*(m*x[i]+c))))
    return f

    



with open('veh0105.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for i in range(8):
        next(reader)
    for row in reader:
        la = row[0]
        if la == '':
            continue
        n = row[1]
        while n[0] == ' ':
            n = n[1:]
        name[la] = n

        try:
            total[la] = float(row[2].replace(',',''))*1000
        except:
            continue

with open('EVregionalSales.csv','r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row[0] == '':
            continue

        la = row[0]

        d = []
        try:
            for i in range(2,len(row)):
                d.append(float(row[len(row)+1-i])/total[la])
        except:
            continue

        data[la] = d
locs = {}
with open(stem+'LA-lat-lon.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[1]] = [float(row[3]),float(row[2])]

gb = [182994,168239,155242,141766,130519,117062,106887,94266,85863,75679,
      67010,56186,49702,43694,8248,30405,25349,20711,18396,16705,15809,15249,
      14465,13937,13184,12735,2205,11900]
_gb = []
for i in range(1,len(gb)+1):
    _gb.append(gb[-i]/32e6)
gb = _gb
print(scurve(gb,[2030]))

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

    if False:#p == 'E06000005':
        fig=plt.figure(figsize=(8,3))
        plt.rcParams["font.family"] = 'serif'
        plt.rcParams['font.size'] = 11
        plt.subplot(1,2,1)
        x = np.arange(2011.75,2018.75,0.25)
        plt.scatter(np.arange(2011.75,2018.75,0.25),data[p],c='k',marker='x')
        plt.ylim(0,0.005)
        plt.yticks(np.arange(0,0.006,0.001),np.arange(0,0.6,0.1))
        plt.plot(x,scurve(data[p],x))
        plt.grid()
        plt.ylabel('Penetration (%)')
        plt.xlabel('Year')
        plt.title('Raw Data',y=0.8)

        logy = []
        logx = []
        for i in range(len(x)):
            logx.append(np.log(x[i]))
            logy.append(np.log(data[p][i]))

        plt.subplot(1,2,2)
        plt.scatter(logx,logy,c='k',marker='x')

        [m,c] = np.polyfit(logx,logy,1)
        f = []
        for i in range(len(logx)):
            f.append(c+m*logx[i])
        plt.plot(logx,f)
        plt.xlim(7.6065,7.6105)
        plt.ylim(-9,-5)
        plt.grid()
        plt.title('Log-log Plot',y=0.8)
        plt.ylabel('Log-Penetration')
        plt.xlabel('Log-Year')
        plt.tight_layout()
        plt.savefig('../../Dropbox/thesis/chapter3/img/scurve2.eps', format='eps', dpi=1000,
                    bbox_inches='tight', pad_inches=0)


        plt.show()
    f = scurve(data[p],years)
    z.append(100*f[0])
    z2.append(100*f[1])
    z3.append(100*f[2])

with open('2030.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['LA','%'])
    for i in range(len(z3)):
        writer.writerow([lalist[i],z3[i]])
# create new figure, axes instances.
'''
fig=plt.figure(figsize=(3,8))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 9
'''
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

x = np.arange(-7,3,0.02)
y = np.arange(49,59,0.02)

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
plt.savefig('../../Dropbox/papers/proposal/evs_scurve.eps', format='eps', dpi=300,
            bbox_inches='tight', pad_inches=0)


plt.show()
        
