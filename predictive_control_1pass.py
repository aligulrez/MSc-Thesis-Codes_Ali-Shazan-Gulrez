#C:\Users\ashaz\Python Trial\battery_bhasam>predictive_control_1pass.py gen.csv 23102012.txt 0
#predictive_control_1pass.py 20100809_15mins.txt 08082019_oahu_demand.txt 1 ebres_08082019.txt
import numpy as np
import matplotlib.pyplot as plt
plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 14}

plt.rc('font', **font)
#plt.rc('xlabel',fontsize=14)
#plt.rc('ylabel',fontsize=14)
from sys import argv
###########################################
############# Constants ###################
###########################################

#Feed in limit in watts
Pfil = 2700
Ncharge = 0.95
Ndischarge = 0.95
# in watts
PB_inv_max = 700
# Battery params
EB_max = 2000 
EB_min = 200
#Time step
delta_t = 15.0/60
with open(argv[1],'r') as pv_file:
	Ppv_i = np.array([float(val)*7.6 for val in pv_file.readline()[:-1].strip().split(',')])
with open(argv[2],'r') as demand_file:
	Pd = np.array([float(val)*2700 for val in demand_file.readline()[:-1].strip().split(',')])
a = int((5*4)+(167/15))
Ppv = []
if(len(Pd) > len(Ppv_i)):
	if(int(argv[3]) == 0):
		for i in range(a):
			Ppv.append(0)
		for val in Ppv_i:
			Ppv.append(val)
		for i in range(len(Pd) - len(Ppv_i) - a):
			Ppv.append(0)
	elif(int(argv[3]) == 1):
		for i in range(20):
			Ppv.append(0)
		for val in Ppv_i:
			Ppv.append(val)
		b= len(Ppv)
		for i in range(len(Pd) - b ):
			Ppv.append(0)

Pfilfc = Ppv - Pd - Pfil

PBres = np.zeros(len(Pfilfc))
for i,val in enumerate(Pfilfc):
	if(val <= 0):
		PBres[i] = 0
		
	elif(val >0 and val < (PB_inv_max*Ncharge)):
		PBres[i] = val
	elif(val >= (PB_inv_max*Ncharge)):
		PBres[i] = PB_inv_max

pow_sum = sum(PBres)
EBres_pot = np.zeros(len(Pfilfc))

for i,val in enumerate(PBres):
	EBres_pot[i] = pow_sum * (delta_t)
	pow_sum -= val
	
EBres = np.zeros(len(Pfilfc))		

for i,val in enumerate(EBres_pot):
	if(val <= (EB_max - EB_min)):
		EBres[i] = val
	elif(val > (EB_max -EB_min)):
		EBres[i] = 0
# z = open(argv[4],'w')
# for val in EBres:
	# z.write(str(val))
	# z.write(',')
# z.close()
if(int(argv[3]) == 1):
	if(len(argv) > 4):
		with open(argv[4],'r') as eb_res_file:
			EBres = np.array([float(val) for val in eb_res_file.readline()[:-1].strip().split(',')])
	else:
		EBres = np.zeros(len(Pfilfc))
delta_EB = 0
delta_EB_pot = 0
PB_pot = 0
Ppot = np.zeros(len(Pfilfc))
EB = np.zeros(len(Pfilfc))
PB = np.zeros(len(Pfilfc))
#Initial condition
Ppot[0] = Ppv[0] - Pd[0]
EB[0] = EB_min
PB[0] = 0
for i in range(1,len(Pfilfc)):
	if(abs(Ppot[i-1]) < PB_inv_max):
		PB_pot = Ppot[i-1]
	else:
                if(Ppot[i-1] < 0):
		        PB_pot = -PB_inv_max
                else:
                        PB_pot = PB_inv_max
		
	if(PB_pot > 0):
		delta_EB_pot = PB_pot * Ncharge * delta_t
	elif(PB_pot <= 0):
		delta_EB_pot = (PB_pot * delta_t)/Ndischarge

	if((EB[i-1] + delta_EB_pot >= EB_min) and (EB[i-1] + delta_EB_pot <= EB_max)):
		delta_EB = delta_EB_pot
	elif(EB[i-1] + delta_EB_pot < EB_min):
		delta_EB = EB_min - EB[i-1]
	elif(EB[i-1] + delta_EB_pot > EB_max):
		delta_EB = EB_max - EB[i-1]
	
	EB[i] = EB[i-1] + delta_EB
	PB[i] = delta_EB/delta_t
	if(EB_max - EBres[i-1] <= EB[i]):
		Ppot[i] = Ppv[i-1] - Pd[i-1] - Pfil
	else:
		Ppot[i] = Ppv[i-1] - Pd[i-1]
PB_inv = np.zeros(len(Pfilfc))
for i,val in enumerate(PB):
	if(val > 0):
		PB_inv[i] = val/Ncharge
	else:
		PB_inv[i] = val*Ndischarge
PR = Ppv - Pd - PB_inv
PG = np.zeros(len(Pfilfc))
for i,val in enumerate(PR):
	if(val <= Pfil):
		PG[i] = val
	else:
		PG[i] = Pfil
Pfil_loss = np.zeros(len(Pfilfc))
for i,val in enumerate(PR):
	if(val - PG[i] > 0):
		Pfil_loss[i] = val - PG[i]
	else:
		Pfil_loss[i] = 0
Pdir_SC = np.zeros(len(Pfilfc))
for i,val in enumerate(Ppv):
	if(val < Pd[i]):
		Pdir_SC[i] = val
	else:
		Pdir_SC[i] = Pd[i]
Pcharge = np.zeros(len(Pfilfc))
for i,val in enumerate(PB_inv):
	if(val > 0):
		Pcharge[i] = val
	else:
		Pcharge[i] = 0
EPV = sum(Ppv) * delta_t
ESC = sum( Pdir_SC + Pcharge ) * delta_t
SCR = ESC/EPV
print "SCR:%f"%(SCR)
Efil_loss = sum(Pfil_loss) * delta_t
CLR = Efil_loss/EPV
print "CLR:%f"%(CLR)
x = [i for i in range(len(Pfilfc))]
fig, axs = plt.subplots(3)
axs[0].plot(x,Ppv,x,Pd,x,PBres)
axs[0].plot(x,[Pfil for i in range(len(Pfilfc))],linestyle='-.',color='#c0c0c0')
axs[0].legend(["$P_{pv}$","$P_d$","$P_{B res}$","$P_{fil}$"],loc="upper right")
axs[1].plot(x,EB,x,EBres)
axs[1].legend(["$E_B$","$E_{B res}$"],loc="upper right")
axs[2].plot(x,PG,x,Pfil_loss)
axs[2].legend(["$P_G$","$P_{FIL loss}$"],loc="upper right",)
axs[0].set(ylabel="Power (W)")
axs[1].set(ylabel="Power (W)")
axs[2].set(ylabel="Power (W)")
plt.xlabel("Time (15 mins)",fontsize=14)
plt.show()
	
	
