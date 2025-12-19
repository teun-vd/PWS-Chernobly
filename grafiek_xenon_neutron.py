import matplotlib.pyplot as plt
import numpy as np

'10 waarden x 3 herhalingen = 30 data punten'

lijst_neutron = [
                100, 100, 100,           #100
                200, 200, 200,           #200
                300, 300, 300,           #300
                400, 400, 400,           #400
                500, 500, 500,           #500
                700, 700, 700,           #700
                900, 900, 900,           #900
                1000,1000,1000,          #1000
                1200,1200,1200,          #1200
                1500,1500,1500,          #1500
                2000,2000,2000 ]         #2000  
lijst_xenon =  [24.15,  28.42,  26.22,   #100
                38.03,  50.26,  40.17,   #200
                53.26,  58.875, 47.89,   #300
                60.14,  69.92,  54.765,  #400
                60.465, 64,     67.015,  #500
                72.765, 77.93,  86.275,  #700
                92.55,  83.83,  86.475,  #900
                99.26,  105.95, 93.355,  #1000
                88.34,  103.37, 95.745,  #1200      
                120.54, 95.785, 115.435, #1500
                105.85, 121.42, 111.505]  #2000

neutron_groups = sorted(set(lijst_neutron))
colors = plt.cm.viridis(np.linspace(0,1,len(neutron_groups)))

plt.figure(figsize=(10,6))

for i, group in enumerate(neutron_groups):
    idx = [j for j, n in enumerate(lijst_neutron) if n == group]
    y_values = [lijst_xenon[j] for j in idx]
    plt.scatter(np.array([lijst_neutron[j] for j in idx]), y_values, color=colors[i], label=f'{group} neutronen', s=60, alpha=0.8)

plt.xlabel('Aantal neutronen')
plt.ylabel('Aantal Xenon-135 kernen')
plt.title('Neutronen en Xenon-135')
plt.legend(title='Neutrongroepen')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()