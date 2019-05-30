import csv
import numpy as np
import copy
import matplotlib.pyplot as plt
import csv
import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.markers as ms


datafile = 'EVmodelParameters.csv'

params = {}
with open(datafile,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        params[row[1]+'-'+row[0]] = [float(row[3]),float(row[4]),float(row[5]),
                                     float(row[6]),float(row[7])]


c1 = params['NISSAN LEAF-2019']
#c2 = params['Jaguar I-PACE-2019']
c2 = params['BMW I3 BEV-2016']

c3 = params['Tesla Model S 60D-2016']

def mpg(c,v):
    v = v*0.277778# m/s
    f = c[1]+c[2]*v+c[3]*v*v # N
    p = f*v # W
    p1 = 1300+p*c[4] # W

    return 1e-3*p1/v

v = np.arange(1,101)
f1 = []
m1 = [[],[1e9]]
f2 = []
m2 = [[],[1e9]]
f3 = []
m3 = [[],[1e9]]
for v_ in v:
    f1.append(mpg(c1,v_))
    if f1[-1] < m1[1][0]:
        m1 = [[v_],[f1[-1]]]
    f2.append(mpg(c2,v_))
    if f2[-1] < m2[1][0]:
        m2 = [[v_],[f2[-1]]]
    f3.append(mpg(c3,v_))
    if f3[-1] < m3[1][0]:
        m3 = [[v_],[f3[-1]]]

plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 14
plt.plot(v,f1,label='Nissan Leaf')
plt.scatter(m1[0],m1[1])
plt.plot(v,f2,label='BMW I3')
plt.scatter(m2[0],m2[1])
plt.plot(v,f3,label='Tesla Model S')
plt.scatter(m3[0],m3[1])
plt.ylabel('Fuel Economy (kJ/m)')
plt.ylim(0.2,0.8)
plt.xlim(0,100)
plt.xlabel('Speed (kmph)')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('../Dropbox/thesis/chapter3/img/fuel_economy.eps',format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0.1)
plt.show()
