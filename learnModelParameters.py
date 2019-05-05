import csv
import numpy as np
import copy
import matplotlib.pyplot as plt

datafile = 'pureEVdataIncCapacity.csv'
outfile = 'EVmodelParameters.csv'

v_h = []
v_u = []
with open('highways.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        v_h.append(float(row[1])*0.277778)
        
with open('UDDS.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        v_u.append(float(row[1])*0.277778)

s_h = copy.deepcopy(sum(v_h)/1000)
s_u = copy.deepcopy(sum(v_u)/1000)

a_h = [0]
a_u = [0]
for i in range(0,len(v_h)-1):
    a_h.append(v_h[i+1]-v_h[i])
for i in range(len(v_u)-1):
    a_u.append(v_u[i+1]-v_u[i])
   
v_params = []
v_obs = []
data = []
with open(datafile,'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        year = row[0]
        model = row[1]
        cap = float(row[2])
        mass = float(row[3])/2.2 #lbs -> kg
        Ta = float(row[4])*4.44822 # convert lbf to N
        Tb = float(row[5])*9.9503 # lbf/mph -> N/mps
        Tc = float(row[6])*22.258 # lbf/mph2 -> N/(mps)^2 
        fe_h = 20.944*s_h/float(row[7])
        fe_u = 20.944*s_u/float(row[8])
        v_params.append([year,model,cap,mass,Ta,Tb,Tc])
        v_obs.append([fe_h,fe_u])

v_forces = []
for v in v_params:
    m = copy.deepcopy(v[3])
    T_a = copy.deepcopy(v[4])
    T_b = copy.deepcopy(v[5])
    T_c = copy.deepcopy(v[6]) 

    F_h = []
    F_u = []
    for value in v_h:
        F_h.append(T_a+T_b*value+T_c*value*value)
    for value in v_u:
        F_u.append(T_a+T_b*value+T_c*value*value)

    for i in range(0,len(a_h)):
        F_h[i] += m*a_h[i]
        F_h[i] = F_h[i]*v_h[i]
    for i in range(0,len(a_u)):
        F_u[i] += m*a_u[i]
        F_u[i] = F_u[i]*v_u[i]
    v_forces.append([F_h,F_u])

    

def _f(x,p0,index):
    f = 0
    F_h = copy.deepcopy(v_forces[index][0])
    F_u = copy.deepcopy(v_forces[index][1])

    E_h = 0
    E_u = 0

    for t in range(len(a_h)):
        if a_h[t] >= 0:
            E_h += F_h[t]/x
        else:
            E_h += F_h[t]*x
        E_h += p0
    E_h = E_h*2.77778e-7 # J -> kWh

    for t in range(len(a_u)):
        if a_u[t] >= 0:
            E_u += F_u[t]/x
        else:
            E_u += F_u[t]*x
        E_u += p0
    E_u = E_u*2.77778e-7 # J -> kWh

    f += abs(E_h-v_obs[index][0])
    f += abs(E_u-v_obs[index][1])

    return f

def learn_eff(p0,index):
    best = None
    lwst = 10000
    for eff in np.arange(0.5,1,0.01):
        f = _f(eff,p0,index)
        if f < lwst:
            lwst = f
            best = eff
    return f,best

best_eff = None
best_p0 = None
lwst = 1000000
for p0 in range(100,1200,100):
    print(p0)
    eff = []
    f = 0
    for v in range(len(v_params)):
        f1,best = learn_eff(p0,v)
        f += f1
        eff.append(best)
    if f < lwst:
        lwst = f
        best_p0 = p0
        best_eff = eff
        
        
results = []
for v in range(len(v_params)):
    results.append(v_parms[v]+[best_eff[v]])
        
        
'''
            
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
for p in range(575,600,1):
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
'''
with open(outfile,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['year','model','capacity (kWh)','mass (kg)','Ta','Tb',
                     'Tc','efficiency'])
    for row in results:
        writer.writerow(row)
