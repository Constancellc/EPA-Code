import csv
import matplotlib.pyplot as plt

u = []
h = []

with open('UDDS.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        u.append(float(row[1]))

with open('highways.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        h.append(float(row[1]))

plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 14
plt.plot(u)
plt.ylabel('Speed (kmph)')
plt.xlabel('Time (s)')
plt.xlim(0,len(u))
plt.tight_layout()
plt.ylim(0,95)
plt.grid(ls=':')
plt.savefig('urban.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0.1)

plt.figure(figsize=(6,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 14
plt.plot(h)
plt.ylabel('Speed (kmph)')
plt.xlabel('Time (s)')
plt.xlim(0,len(h))
plt.tight_layout()
plt.ylim(0,100)
plt.grid(ls=':')
plt.savefig('highways.eps', format='eps',
            dpi=1000, bbox_inches='tight', pad_inches=0.1)
plt.show()
