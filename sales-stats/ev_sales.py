import csv
import matplotlib.pyplot as plt
import numpy as np


fitStart = 55

plotMax = 2040
EVlifetime = 10*12

y_ev = []
y_grant = []

total = []

with open('ev_sales.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        y_ev.append(float(row[2])/float(row[4]))
        y_grant.append(float(row[3])/float(row[4]))
        total.append(float(row[4]))

vpm = sum(total)/len(total)
y = []
for i in range(0,len(y_grant)):
    y.append(y_grant[len(y_grant)-1-i])

inv = []
for i in range(0,len(y)):
    inv.append(np.log(y[i]/(1-y[i])))

[m,c] = np.polyfit(range(fitStart,len(y)),inv[fitStart:],1)

def scurve(x):
    st = m*x+c
    return 1/(1+np.exp(-st))

s = []
for i in range(0,520):
    s.append(scurve(i))

newEVs = []
for i in range(0,len(s)):
    newEVs.append(s[i]*vpm)

nEVs = [newEVs[0]]
for i in range(1,EVlifetime):
    nEVs.append(nEVs[-1]+newEVs[i])
for i in range(EVlifetime,len(s)):
    nEVs.append(nEVs[-1]+newEVs[i]-newEVs[i-EVlifetime])

for i in range(0,len(nEVs)):
    nEVs[i] = nEVs[i]/1000000
    
invfit = []
for i in range(0,len(y)+10):
    invfit.append(m*i+c)

plt.figure(figsize=(10,8))

ax2 = plt.subplot2grid((3,2),(0,0),colspan=1)
ax1 = plt.subplot2grid((3,2),(0,1),colspan=1)
ax3 = plt.subplot2grid((3,2),(1,0),colspan=2,rowspan=2)
ax4 = ax3.twinx()

ax1.set_title('Training data fit',y=0.8)
ax1.plot(range(0,len(y)),y,c='k',label='Observed Data')
ax1.plot(range(0,len(s)),s,label='S Curve')
ax1.set_xlim(0,9*12)
ax1.set_ylim(0,0.04)
ax1.set_xticks(range(4,9*12+4,12))
ax1.set_xticklabels(['2011','2012','2013','2014','2015','2016','2017','2018',
                     '2019'])
ax1.grid()
ax1.legend(loc=[-0.5,1.1],ncol=2)

#ax2.subplot(1,2,2)
ax2.set_title('Fitting the S-Curve',y=0.8)
ax2.scatter(range(len(y)),inv,c='k',marker='x')
ax2.plot(invfit)
ax2.set_xticks(range(4,9*12+4,12))
ax2.set_xticklabels(['2011','2012','2013','2014','2015','2016','2017','2018',
                     '2019'])
ax2.set_ylim(-11,-2)
ax2.set_xlim(0,9*12)
ax2.grid()

ax3.plot(range(0,len(s)),s)
ax3.scatter(range(0,len(y)),y,c='k',marker='x')
ax3.set_title('Projected EV Numbers',y=0.9)
ax3.set_xticks(range(52,52+60*8,60))
ax3.set_xticklabels(['2015','2020','2025','2030','2035','2040','2045','2050'])
ax3.tick_params('y',labelcolor='C0')
ax3.set_yticks(np.arange(0.0,1.2,0.2))
ax3.set_yticklabels(['0%','20%','40%','60%','80%','100%'])
ax3.set_xlim(50,355)
#ax3.set_xlim(50,500)
ax3.set_ylabel('Percentage of new vehicle sales',color='C0')
ax3.set_ylim(0,1.1)
ax3.grid()

ax4.plot(range(0,len(s)),nEVs,'g')
ax4.set_ylim(0,27.5)
ax4.set_ylabel('Millions of EVs on road',color='g')
ax4.tick_params('y', colors='g')

plt.tight_layout()


# Now let's see just pure evs


vpm = sum(total)/len(total)
y = []
for i in range(0,len(y_ev)):
    y.append(y_ev[len(y_ev)-1-i])

inv = []
for i in range(0,len(y)):
    inv.append(np.log(y[i]/(1-y[i])))

[m,c] = np.polyfit(range(fitStart,len(y)),inv[fitStart:],1)

def scurve(x):
    st = m*x+c
    return 1/(1+np.exp(-st))

s = []
for i in range(0,520):
    s.append(scurve(i))

newEVs = []
for i in range(0,len(s)):
    newEVs.append(s[i]*vpm)

nEVs = [newEVs[0]]
for i in range(1,EVlifetime):
    nEVs.append(nEVs[-1]+newEVs[i])
for i in range(EVlifetime,len(s)):
    nEVs.append(nEVs[-1]+newEVs[i]-newEVs[i-EVlifetime])

for i in range(0,len(nEVs)):
    nEVs[i] = nEVs[i]/1000000
    
invfit = []
for i in range(0,len(y)+10):
    invfit.append(m*i+c)

plt.figure(figsize=(10,8))

ax2 = plt.subplot2grid((3,2),(0,0),colspan=1)
ax1 = plt.subplot2grid((3,2),(0,1),colspan=1)
ax3 = plt.subplot2grid((3,2),(1,0),colspan=2,rowspan=2)
ax4 = ax3.twinx()

ax1.set_title('Training data fit',y=0.8)
ax1.plot(range(0,len(y)),y,c='k',label='Observed Data')
ax1.plot(range(0,len(s)),s,label='S Curve')
ax1.set_xlim(0,8.9*12)
ax1.set_ylim(0,0.04)
ax1.set_xticks(range(4,9*12+4,12))
ax1.set_xticklabels(['2011','2012','2013','2014','2015','2016','2017','2018',
                     '2019'])
ax1.grid()
ax1.legend(loc=[-0.5,1.1],ncol=2)

#ax2.subplot(1,2,2)
ax2.set_title('Fitting the S-Curve',y=0.8)
ax2.scatter(range(len(y)),inv,c='k',marker='x')
ax2.plot(invfit)
ax2.set_xticks(range(4,9*12+4,12))
ax2.set_xticklabels(['2011','2012','2013','2014','2015','2016','2017','2018',
                     '2019'])
ax2.set_ylim(-11,-2)
ax2.set_xlim(0,8.9*12)
ax2.grid()

ax3.plot(range(0,len(s)),s)
ax3.scatter(range(0,len(y)),y,c='k',marker='x')
ax3.set_title('Projected EV Numbers',y=0.9)
ax3.set_xticks(range(52,52+60*8,60))
ax3.set_xticklabels(['2015','2020','2025','2030','2035','2040','2045','2050'])
ax3.tick_params('y',labelcolor='C0')
ax3.set_yticks(np.arange(0.0,1.2,0.2))
ax3.set_yticklabels(['0%','20%','40%','60%','80%','100%'])
ax3.set_xlim(50,355)
#ax3.set_xlim(50,500)
ax3.set_ylabel('Percentage of new vehicle sales',color='C0')
ax3.set_ylim(0,1.1)
ax3.grid()

ax4.plot(range(0,len(s)),nEVs,'g')
ax4.set_ylim(0,27.5)
ax4.set_ylabel('Millions of EVs on road',color='g')
ax4.tick_params('y', colors='g')

plt.tight_layout()
plt.show()
'''

for i in range(0,len(x)):
    x[i] = len(y_ev)-x[i]


plt.figure(1)
plt.scatter(np.arange(len(y_ev),0,-1),y_ev)
plt.scatter(np.arange(len(y_grant),0,-1),y_grant)
plt.xticks(x,x_ticks)
plt.ylim(0,2.2)
plt.xlim(1,len(y_ev)+1)
plt.grid()
plt.show()
'''
