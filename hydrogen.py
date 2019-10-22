import csv
import matplotlib.pyplot as plt
import numpy as np
import copy


e = [42,22,40,1,-11,-80,46,12]
g = [54,38,52,16,-21,-62,100,100]

plt.figure(figsize=(8,3))
plt.rcParams["font.family"] = 'serif'
plt.rcParams['font.size'] = 11
plt.bar(np.arange(0,8)-0.2,e,width=0.4,zorder=2,label='Energy',edgecolor='black',)
plt.bar(np.arange(0,8)+0.2,g,width=0.4,zorder=2,label='Emissions',edgecolor='black', hatch="//")
plt.xticks(range(8),['Natural Gas\n(Central,G)','Natural Gas\n(Central,L)',
                     'Natural Gas\n(Station,G)','Natural Gas\n(Station,L)',
                     'Electrolysis\n(US Mix,G)','Electrolysis\n(US Mix,L)',
                     'Electrolysis\n(Renew,G)','Electrolysis\n(Renew,L)'],
           rotation=90)
plt.grid(zorder=0)
plt.ylabel('Reduction compared to\npetrol vehicles (%)')
plt.legend()
plt.tight_layout()
plt.savefig('hydrogen.pdf',format='pdf',dpi=300)





plt.figure(figsize=(5.8,2.6))
plt.rcParams['font.size'] = 12
e = [-11,-18,-6]
g = [82.5,91,14]
plt.bar(np.arange(0,3)-0.2,e,width=0.4,zorder=2,label='Energy',edgecolor='black',)
plt.bar(np.arange(0,3)+0.2,g,width=0.4,zorder=2,label='Emissions',edgecolor='black', hatch="//")
plt.xticks(range(3),['CBG\n(TG)','CBG\n(AG)','CNG'],rotation=90)
plt.plot([0.2,0.2],[75,90],c='k',lw=3)
plt.plot([1.2,1.2],[83,99],c='k',lw=3)
plt.grid(zorder=0)
plt.ylabel('Reduction compared to\npetrol vehicles (%)')
plt.legend()
plt.tight_layout()
plt.savefig('biogas.pdf',format='pdf',dpi=300)

plt.figure(figsize=(5.8,3))
plt.rcParams['font.size'] = 12
e = [64]*4
g = [28,89,-3,6]
plt.bar(np.arange(0,4)-0.2,e,width=0.4,zorder=2,label='Energy',edgecolor='black',)
plt.bar(np.arange(0,4)+0.2,g,width=0.4,zorder=2,label='Emissions',edgecolor='black', hatch="//")
plt.xticks(range(4),['US\nMix','French\nMix','China\nMix','India\nMix'],rotation=90)
plt.grid(zorder=0)
plt.ylabel('Reduction compared to\npetrol vehicles (%)')
plt.ylim(-10,105)
plt.legend()
plt.tight_layout()
plt.savefig('electric.pdf',format='pdf',dpi=300)

plt.show()
