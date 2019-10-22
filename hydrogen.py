import csv
import matplotlib.pyplot as plt
import numpy as np
import copy

petrol_C02 = 350
petrol_kWh = 1.04

e = [42,22,40,1,-11,-80,46,12]
g = [54,38,52,16,-21,-62,100,100]

y1 = [petrol_C02]
y2 = [petrol_kWh]

for i in range(len(g)):
    y1.append(y1[0]*(1-g[i]/100))
    y2.append(y2[0]*(1-e[i]/100))
    
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 11
#plt.figure(figsize=(8,3))
fig, ax1 = plt.subplots(figsize=(8,4))

plt.xticks(rotation=90)
ax1.set_ylabel('Energy Consumption kWh/mile', color='#1f77b4')
ax1.bar(np.arange(0,9)-0.2,y2,width=0.4,zorder=2,edgecolor='black',)
ax1.plot([-1,10],[petrol_kWh,petrol_kWh],ls=':',c='#1f77b4')
ax1.tick_params(axis='y', labelcolor='#1f77b4')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis


ax2.set_ylabel('GHG emissions ($C0_2$e g/mile)', color='#ff7f0e')  # we already handled the x-label with ax1
ax2.bar(np.arange(0,9)+0.2,y1,width=0.4,zorder=2,label='Emissions',edgecolor='black', hatch="//",color='#ff7f0e')
ax2.tick_params(axis='y', labelcolor='#ff7f0e')

ax2.plot([-1,10],[petrol_C02,petrol_C02],ls=':',c='#ff7f0e')
plt.xticks(range(9),['Petrol\nICE','$H_2$-Natural Gas\n(Central,G)','$H_2$-Natural Gas\n(Central,L)',
                     '$H_2$-Natural Gas\n(Station,G)','$H_2$-Natural Gas\n(Station,L)',
                     '$H_2$-Electrolysis\n(US Mix,G)','$H_2$-Electrolysis\n(US Mix,L)',
                     '$H_2$-Electrolysis\n(Renew,G)','$H_2$-Electrolysis\n(Renew,L)'])

plt.xlim(-0.8,8.8)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('hydrogen.pdf',format='pdf',dpi=300)





plt.rcParams['font.size'] = 12
e = [-11,-18,-6]
g = [82.5,91,14]

y1 = [petrol_C02]
y2 = [petrol_kWh]

for i in range(len(g)):
    y1.append(y1[0]*(1-g[i]/100))
    y2.append(y2[0]*(1-e[i]/100))


fig, ax1 = plt.subplots(figsize=(5.8,3.5))

plt.xticks(rotation=90)
ax1.set_ylabel('Energy Consumption kWh/mile', color='#1f77b4')
ax1.bar(np.arange(0,4)-0.2,y2,width=0.4,zorder=2,edgecolor='black',)
ax1.plot([-1,10],[petrol_kWh,petrol_kWh],ls=':',c='#1f77b4')
ax1.tick_params(axis='y', labelcolor='#1f77b4')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis


ax2.set_ylabel('GHG emissions ($C0_2$e g/mile)', color='#ff7f0e')  # we already handled the x-label with ax1
ax2.bar(np.arange(0,4)+0.2,y1,width=0.4,zorder=2,label='Emissions',edgecolor='black', hatch="//",color='#ff7f0e')
ax2.tick_params(axis='y', labelcolor='#ff7f0e')

ax2.plot([-1,10],[petrol_C02,petrol_C02],ls=':',c='#ff7f0e')
plt.xticks(range(4),['Petrol\nICE','CBG\n(TG)','CBG\n(AG)','CNG'])

plt.xlim(-0.7,3.7)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('biogas.pdf',format='pdf',dpi=300)





e = [64]*4
g = [28,89,-3,6]

y1 = [petrol_C02]
y2 = [petrol_kWh]

for i in range(len(g)):
    y1.append(y1[0]*(1-g[i]/100))
    y2.append(y2[0]*(1-e[i]/100))


fig, ax1 = plt.subplots(figsize=(5.8,4))

plt.xticks(rotation=90)
ax1.set_ylabel('Energy Consumption kWh/mile', color='#1f77b4')
ax1.bar(np.arange(0,5)-0.2,y2,width=0.4,zorder=2,edgecolor='black',)
ax1.plot([-1,10],[petrol_kWh,petrol_kWh],ls=':',c='#1f77b4')
ax1.tick_params(axis='y', labelcolor='#1f77b4')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis


ax2.set_ylabel('GHG emissions ($C0_2$e g/mile)', color='#ff7f0e')  # we already handled the x-label with ax1
ax2.bar(np.arange(0,5)+0.2,y1,width=0.4,zorder=2,label='Emissions',edgecolor='black', hatch="//",color='#ff7f0e')
ax2.tick_params(axis='y', labelcolor='#ff7f0e')

ax2.plot([-1,10],[petrol_C02,petrol_C02],ls=':',c='#ff7f0e')
plt.xticks(range(5),['Petrol\nICE','EV-US\nMix','EV-French\nMix','EV-China\nMix','EV-India\nMix'])

plt.xlim(-0.7,4.7)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('electric.pdf',format='pdf',dpi=300)
plt.show()

