from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook
import csv

stem = '../simulation_results/NTS/clustering/power/locationsLA_/'

total = {}
_2018 = {}
name = {}

with open('veh0105.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    for row in reader:
        if row[0] == '':
            continue
        if row[0][0] not in ['E','S','W']:
            continue
        total[row[0]] = float(row[2].replace(',',''))*1000
        name[row[0]] = row[1]
        if name[row[0]][-3:] == ' UA':
            name[row[0]] = name[row[0]][:-3]

with open('EVregionalSales.csv','r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == '':
            continue
        if row[0][:1] not in ['E','S','W']:
            continue
        try:
            _2018[row[0]] = float(row[2])/total[row[0]]
        except:
            continue
        
# create new figure, axes instances.
fig=plt.figure(figsize=(6,8) )
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 8
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=-7,llcrnrlat=49.9,urcrnrlon=2.2,urcrnrlat=58.7,\
            resolution='h',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)


#            rsphere=(6378137.00,6356752.3142),\
# get locations
locs = {}
with open(stem+'LA-lat-lon.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        locs[row[1]] = [float(row[3]),float(row[2])]

pList = []
z = []

for p in _2018:
    try:
        pList.append(locs[p])
    except:
        continue
    z.append(100*_2018[p])
    if z[-1] > 2:
        print(z[-1])
        print(p)
        print('')

        
'''    
for l in locs:
    try:
    with open(stem+l+'.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            pList.append(locs[row[0]])
            z.append(100*(float(row[2])-float(row[1]))/float(row[1]))
'''
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

# make these smaller to increase the resolution
x = np.arange(-7,3,0.02)
y = np.arange(49,59,0.02)

Z = np.zeros((len(x),len(y)))
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
        else:
            continue

m.pcolor(X,Y,Z,vmax=2)#,cmap='inferno')
#m.pcolormesh(x,y,Z,latlon=True)
#m.drawmapboundary(fill_color='#99ffff')
#m.drawlsmask(land_color='coral',ocean_color='aqua')
# draw parallels
#m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# draw meridians
#m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
plt.colorbar()
plt.show()
