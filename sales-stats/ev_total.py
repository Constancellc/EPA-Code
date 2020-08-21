import csv
import matplotlib.pyplot as plt
import numpy as np


fitStart = 1#55

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
        y_grant.append(float(row[3]))
        total.append(float(row[4]))
y_grant = list(reversed(y_grant))

cum_per = [0]
for x in y_grant:
    cum_per.append(cum_per[-1]+x/32000000)
    
inv = []
for i in range(0,len(cum_per)):
    inv.append(np.log(cum_per[i]/(1-cum_per[i])))

[m,c] = np.polyfit(range(50,len(inv)),inv[50:],1)
print([m,c])
def scurve(x):
    st = m*x+c
    return 1/(1+np.exp(-st))

first3_5=None
first7=None
s = []
for i in range(0,520):
    s.append(32000*scurve(i))
    if s[i] > 2485.714 and first3_5 is None:
        first3_5 = i 
    if s[i] > 1242.857 and first7 is None:
        first7 = i 
        

existing = [0]
for x in y_grant:
    existing.append(existing[-1]+x/1e3)
    
plt.figure()
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'
plt.plot(s)
plt.scatter(range(len(y_grant)),existing[1:],c='k',marker='x')
plt.plot([first3_5,first3_5],[0,2485.714],c='g',ls='--',label='3.5 kW chargers')
plt.plot([0,first3_5],[2485.714,2485.714],c='g',ls='--')
plt.plot([first7,first7],[0,1242.857],c='m',ls='--')
plt.plot([0,first7],[1242.857,1242.857],c='m',ls='--',label='7 kW chargers')
plt.xticks(range(16,9*24+16,24),['2012','2014','2016','2018','2020','2022',
                                 '2024','2026','2028'])
plt.xlim(52,52+60*2.5)
plt.ylim(0,5000)
plt.ylabel('Number of EVs (000s)')
plt.grid(ls=':')
plt.legend()
plt.tight_layout()
plt.show()

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

plt.figure(figsize=(10,4))
plt.rcParams["font.family"] = 'serif'
plt.rcParams["font.size"] = '10'

plt.subplot(1,2,1)
plt.xticks(range(16,9*24+16,24),['2012','2014','2016','2018','2020','2022',
                                 '2024','2026','2028'])
plt.fill_between(range(0,len(y)),y,color='#AAFFAA',zorder=2,label='PHEVs')
plt.plot(range(0,len(y)),y,c='k',zorder=2)
plt.subplot(1,2,2)
plt.fill_between(range(0,len(s)),s,color='#AAFFAA',zorder=2)

plt.plot(range(0,len(s)),s,c='k',zorder=2)


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
    s.append(100*scurve(i))

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



plt.subplot(1,2,1)
plt.yticks(np.arange(0,0.38,0.05),np.arange(0,40,5))
plt.ylim(0,0.4)
plt.ylabel('Percentage of New Sales')
plt.title('Observed')
plt.xticks(range(4,10*12+4,12),['2011','2012','2013','2014','2015','2016','2017',
                               '2018','2019','2020'])
plt.fill_between(range(0,len(y)),y,color='#AAAAFF',zorder=2,
                 label='BEVs')
plt.plot(range(0,len(y)),y,c='k',zorder=2)
plt.grid(zorder=0)
plt.legend(loc=2)
plt.xlim(0,len(y)-1)

plt.subplot(1,2,2)
plt.ylim(0,100)
plt.xlim(0,len(s)-1)
plt.title('Forecast')
plt.fill_between(range(0,len(s)),s,color='#AAAAFF',zorder=3)
plt.plot(range(0,len(s)),s,c='k',zorder=3)
plt.grid(zorder=0)
plt.xticks(range(52,52+60*8,60),['2015','2020','2025','2030','2035','2040',
                                  '2045','2050'])
plt.tight_layout()

plt.savefig('../../Documents/forecast.jpg', format='jpg', dpi=300,
            bbox_inches='tight', pad_inches=0.1)
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
