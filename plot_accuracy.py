import csv
import numpy as np
import copy
import matplotlib.pyplot as plt

datafile = 'pureEVdataIncCapacity.csv'
params = 'EVmodelParameters.csv'

data = []
with open(datafile,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        data.append(row) # year, model, capacity, weight, Ta-Tc, h fe, u fe

highways = []
urban = []
with open('highways.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        highways.append(float(row[1])*0.277778)
        
with open('UDDS.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        urban.append(float(row[1])*0.277778)

def fit(m,T_a,T_b,T_c,fe_h,fe_u,p0):
    #p0 = 1070 # J/s
    T_a = T_a*4.44822 # convert lbf to N
    T_b = T_b*9.9503 # lbf/mph -> N/mps
    T_c = T_c*22.258 # lbf/mph2 -> N/(mps)^2 

    v_h = copy.copy(highways)
    v_u = copy.copy(urban)

    s_h = sum(v_h)/1000 # km
    s_u = sum(v_u)/1000 # km

    a_h = [0]
    a_u = [0]

    for i in range(0,len(v_h)-1):
        a_h.append(v_h[i+1]-v_h[i])
    for i in range(len(v_u)-1):
        a_u.append(v_u[i+1]-v_u[i])

    F_h = []
    F_u = []
    for value in v_h:
        F_h.append(T_a + T_b*value + T_c*value*value)
    for value in v_u:
        F_u.append(T_a + T_b*value + T_c*value*value)

    for i in range(0,len(a_h)):
        F_h[i] += m*a_h[i]
        F_h[i] = F_h[i]*v_h[i]
    for i in range(0,len(a_u)):
        F_u[i] += m*a_u[i]
        F_u[i] = F_u[i]*v_u[i]

    best = None
    smallest = 100000000
    
    y_h = 20.944*s_h/fe_h # observed - kWh
    y_u = 20.944*s_u/fe_u # observed - kWh
    
    y = y_h+y_u

    for eff in np.arange(0.5,1,0.001):
        E = 0
        
        for i in range(len(a_h)):
            if a_h[i] >= 0:
                E += copy.copy(F_h[i])/eff
            else:
                E += copy.copy(F_h[i])*eff
            E += p0
            
        for i in range(len(a_u)):
            if a_u[i] >= 0:
                E += copy.copy(F_u[i])/eff
            else:
                E += copy.copy(F_u[i])*eff
            E += p0
            
        E = E*2.77778e-7 # J -> kWh

        if abs(E-y) < smallest:
            smallest = abs(E-y)
            best = eff

    return best, smallest


results = []
tot = []
for p in [587]:#range(575,600,1):
    se = 0
    for row in data:
        year = row[0]
        model = row[1]
        cap = float(row[2])
        mass = float(row[3])/2.2 #lbs -> kg
        Ta = float(row[4])
        Tb = float(row[5])
        Tc = float(row[6])
        fe_h = float(row[7])
        fe_u = float(row[8])

        eff,err = fit(mass,Ta,Tb,Tc,fe_h,fe_u,p)
        se += err


        results.append([year,model,cap,mass,Ta,Tb,Tc,eff])
    
    tot.append(se)

plt.figure(1)
plt.plot(range(575,600,1),tot)
plt.show()

print(tot)
with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['year','model','capacity (kWh)','mass (kg)','Ta','Tb',
                     'Tc','efficiency'])
    for row in results:
        writer.writerow(row)
