import matplotlib.pyplot as plt
import csv
import scipy.stats as st
# arbitrary counter so there is somethng to watch on terminal
c=1

# where we're writing to
out = 'pureEVdata.csv'

data = ['EPA/10tstcar.csv','EPA/11tstcar.csv','EPA/12tstcar.csv',\
        'EPA/13tstcar.csv','EPA/14tstcar.csv','EPA/15tstcar.csv',\
        'EPA/16tstcar.csv','EPA/17tstcar.csv','EPA/18tstcar.csv',
        'EPA/19tstcar.csv']

# Older years have slightly different headings :(
older = ['EPA/10tstcar.csv','EPA/11tstcar.csv','EPA/12tstcar.csv',\
        'EPA/13tstcar.csv']

v = []
ta = []
tb = []
tc = []
m = []

for year in data:
    new = []
    with open(year, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row[5] in v:
                continue
            try:
                if year in older:
                    ta.append(float(row[51]))
                    tb.append(float(row[52]))
                    tc.append(float(row[53]))
                else:
                    ta.append(float(row[54]))
                    tb.append(float(row[55]))
                    tc.append(float(row[56]))
            except:
                continue
            v.append(row[5])
            m.append(float(row[21]))

plt.figure(figsize=(10,3.5))

plt.subplot(1,3,1)
plt.scatter(m,ta,marker='x')
plt.ylabel('Ta')
plt.xlabel('Mass')
c,p = st.pearsonr(m,ta)
plt.title('correlation: '+str(round(c,2)))
plt.grid()
plt.xlim(0,9000)
plt.ylim(0,90)

plt.subplot(1,3,2)
plt.scatter(m,tb,marker='x')
c,p = st.pearsonr(m,tb)
plt.title('correlation: '+str(round(c,2)))
plt.ylabel('Tb')
plt.xlabel('Mass')
plt.ylim(-1,2)
plt.xlim(0,9000)
plt.grid()

plt.subplot(1,3,3)
plt.ylim(0,0.06)
plt.scatter(m,tc,marker='x')
c,p = st.pearsonr(m,tc)
plt.title('correlation: '+str(round(c,2)))
plt.ylabel('Tc')
plt.xlabel('Mass')
plt.xlim(0,9000)
plt.grid()

plt.tight_layout()
plt.show()
