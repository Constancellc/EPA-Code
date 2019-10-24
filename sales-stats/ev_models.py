import csv
import matplotlib.pyplot as plt
import numpy as np
import random



leafs = [0]*18
bmwi3 = [0]*18
tesla = [0]*18
imiev = [0]*18
ipace = [0]*18
soul = [0]*18
egolf = [0]*18
zoe = [0]*18


total = []
with open('../../Documents/veh0120_.csv','r+', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        if row[0] == 'Make':
            header = row
        if row[0] == 'NISSAN' and row[1][:4] == 'LEAF':
            total.append(row)
            for i in range(18):
                try:
                    leafs[i] += int(row[2+i])
                except:
                    continue
        if row[0] == 'BMW' and row[1][:2] == 'I3':
            total.append(row)
            for i in range(18):
                try:
                    bmwi3[i] += int(row[2+i])
                except:
                    continue

        if row[0] == 'TESLA':
            total.append(row)
            for i in range(18):
                try:
                    tesla[i] += int(row[2+i])
                except:
                    continue
                
        if row[0] == 'MITSUBISHI' and row[1][:6] == 'I-MIEV':
            total.append(row)
            for i in range(18):
                try:
                    imiev[i] += int(row[2+i])
                except:
                    continue

        if row[0] == 'JAGUAR' and row[1][:6] == 'I-PACE':
            total.append(row)
            for i in range(18):
                try:
                    ipace[i] += int(row[2+i])
                except:
                    continue

        if row[0] == 'KIA' and row[1][:7] == 'SOUL EV':
            total.append(row)
            for i in range(18):
                try:
                    soul[i] += int(row[2+i])
                except:
                    continue

        if row[0] == 'VOLKSWAGEN' and row[1][:6] == 'E-GOLF':
            total.append(row)
            for i in range(18):
                try:
                    egolf[i] += int(row[2+i])
                except:
                    continue

        if row[0] == 'RENAULT' and row[1][:3] == 'ZOE':
            total.append(row)
            for i in range(18):
                try:
                    zoe[i] += int(row[2+i])
                except:
                    continue

with open('leading_models.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for row in total:
        writer.writerow(row)
        
other = [0]*18
plt.figure()
plt.fill_between(np.arange(18,0,-1),[0]*18,leafs,label='Nissan Leaf')
for i in range(18):
    tesla[i] += leafs[i]
plt.fill_between(np.arange(18,0,-1),leafs,tesla,label='Tesla')
for i in range(18):
    bmwi3[i] += tesla[i]
plt.fill_between(np.arange(18,0,-1),tesla,bmwi3,label='BMW I3')
for i in range(18):
    zoe[i] += bmwi3[i]
plt.fill_between(np.arange(18,0,-1),bmwi3,zoe,label='Renault ZOE')
for i in range(18):
    #other[i] += bmwi3[i]
    other[i] += ipace[i]
    other[i] += soul[i]
    other[i] += zoe[i]
    other[i] += egolf[i]
plt.fill_between(np.arange(18,0,-1),zoe,other,label='Other')
plt.legend(loc=2)
plt.xticks(np.arange(2,22,4),['2015','2016','2017','2018','2019'])
plt.xlim(1,18)
plt.ylim(0,62000)
plt.ylabel('Number of EVs')
plt.grid()
plt.show()
