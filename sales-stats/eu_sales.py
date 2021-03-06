import csv
import matplotlib.pyplot as plt
import numpy as np
import random

total = {}
_2017 = {}
_2018 = {}

with open('eu-sales.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    next(reader)
    for row in reader:
        total[row[0]] = int(row[-2].replace(',',''))
        _2017[row[0]] = float(row[-3])
        _2018[row[0]] = float(row[-4])

clrs = ['#ff0000','#ff4000','#ff8000','#ffbf00','#ffff00','#bfff00','#80ff00',
        '#40ff00','#00ff00','#00ff40','#00ff80','#00ffbf','#00ffff','#00bfff',
        '#0080ff','#0040ff','#0000ff','#4000ff','#8000ff','#bf00ff','#ff00ff',
        '#ff00bf','#ff0080','#ff0040','#ff0000']


plt.figure(figsize=(14,6))
for c in total:
    i = int(random.random()*len(clrs))
    plt.scatter([np.log(_2018[c])],[100*(_2018[c]-_2017[c])/_2017[c]],
                total[c]/1000,clrs[i],alpha=0.5)
    plt.annotate(c,(np.log(_2018[c]),100*(_2018[c]-_2017[c])/_2017[c]),
                 (np.log(_2018[c])+np.sqrt(total[c]/100000000),
                  100*(_2018[c]-_2017[c])/_2017[c]+total[c]/100000),
                 color=clrs[i])
plt.xticks([np.log(0.2),np.log(0.5),np.log(1),np.log(2),np.log(5),
            np.log(10),np.log(20),np.log(50)],
           ['0.2','0.5','1','2','5','10','20','50'])
plt.ylabel('% Change from Last Year')
plt.xlabel('% New Sales Electric (2018)')
plt.grid()
plt.tight_layout()
plt.show()
        
