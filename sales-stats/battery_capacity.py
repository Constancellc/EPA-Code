import csv
import matplotlib.pyplot as plt
import numpy as np


y_ev = []
y_grant = []
total = []
t = []
with open('ev_sales.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        t.append(row[0][2:]+row[1])
        y_ev.append(float(row[2]))
        y_grant.append(float(row[3]))
        total.append(float(row[4]))
print(t)
data = []
with open('ev-models.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row[1:])

bev_capacity = {}
for i in range(5):
    tot = 0
    mean = 0
    for j in range(len(data)-1):
        tot += float(data[j+1][i+1])
        mean += float(data[j+1][i+1])*float(data[j+1][0])
    bev_capacity[data[0][i+1]] = mean/tot

print(bev_capacity)
data = []
with open('phev-models.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row[1:])

phev_capacity = {}
for i in range(5):
    tot = 0
    mean = 0
    for j in range(len(data)-1):
        tot += float(data[j+1][i+1])
        mean += float(data[j+1][i+1])*float(data[j+1][0])
    phev_capacity[data[0][i+1]] = mean/tot

print(phev_capacity)
        
cap = [0.0]*len(t)
for i in range(len(t)):
    if t[i][:2] in ['16','15','14','13','12','11','10']:
        cap[i] += y_ev[i]*bev_capacity['16-3']
        cap[i] += (y_grant[i]-y_ev[i])*phev_capacity['16-3']
    elif t[i][:2] == '18':
        cap[i] += y_ev[i]*bev_capacity['18-1']
        cap[i] += (y_grant[i]-y_ev[i])*phev_capacity['18-1']
    elif t[i][2:5] in ['Jan','Feb','Mar']:
        cap[i] += y_ev[i]*bev_capacity['17-1']
        cap[i] += (y_grant[i]-y_ev[i])*phev_capacity['17-1']
    elif t[i][2:5] in ['Apr','May','Jul']:
        cap[i] += y_ev[i]*bev_capacity['17-2']
        cap[i] += (y_grant[i]-y_ev[i])*phev_capacity['17-2']
    else:
        cap[i] += y_ev[i]*bev_capacity['17-2']
        cap[i] += (y_grant[i]-y_ev[i])*phev_capacity['17-2']

cap = list(reversed(cap))
x = np.arange(4,4+12*8,12)
x_ticks = []
for i in range(2011,2019):
    x_ticks.append(str(i))

cum = [0.0]*len(cap)
cum[0] = cap[-1]
for i in range(1,len(cap)):
    cum[i] = cum[i-1]+cap[i]
for i in range(len(cum)):
    cum[i] = cum[i]/1000000

'''
plt.figure()
plt.plot(cum)
plt.xlim(0,len(cum)-1)
plt.ylim(0,3)
plt.ylabel('Fleet Battery Capacity (GWh)')
plt.xticks(x,x_ticks)
plt.grid()
plt.show()
'''

plt.figure(figsize=(10,8))
plt.rcParams["font.family"] = 'serif'
ax2 = plt.subplot2grid((3,2),(0,0),colspan=1)
ax1 = plt.subplot2grid((3,2),(0,1),colspan=1)
ax3 = plt.subplot2grid((3,2),(1,0),colspan=2,rowspan=2)

ax3.plot(cum)
ax3.set_xticks(x)
ax3.set_xticklabels(x_ticks)
ax3.set_xlim(0,len(cum)-1)
ax3.set_ylabel('Fleet Battery Capacity (GWh)')
ax3.set_ylim(0,3.2)
ax3.grid()



pureEVs = {}
with open('ev_sales.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if float(row[0]) not in pureEVs:
            pureEVs[float(row[0])] = float(row[3])
        else:
            pureEVs[float(row[0])] += float(row[3])

print(pureEVs)
t = range(2011,2019)
y = [0.0]
for i in range(len(t)):
    y.append((y[-1]*1000+pureEVs[t[i]])/1000)

ax2.bar(t,y[1:],color='b',zorder=2,label='Hybrids')
ax2.set_ylabel('Thousands of Vehicles')
ax2.set_xlabel('Year')
ax2.set_title('Plug-Ins')
ax2.grid(zorder=0.5)



pureEVs = {}

with open('ev_sales.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if float(row[0]) not in pureEVs:
            pureEVs[float(row[0])] = float(row[2])
        else:
            pureEVs[float(row[0])] += float(row[2])

t = range(2011,2019)
y = [0.0]
for i in range(len(t)):
    y.append((y[i]*1000+pureEVs[t[i]])/1000)

ax1.bar(t,y[1:],zorder=2)
ax2.bar(t,y[1:],color='c',zorder=2,label='BEVs')
ax2.legend()
ax1.set_title('Pure EVs')
ax1.set_ylabel('Thousands of Vehicles')
ax1.set_xlabel('Year')
ax1.grid(zorder=0.5)

plt.tight_layout()
plt.show()
    

    

