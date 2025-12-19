#Import alle modules
import random
import math
import time
import matplotlib.pyplot as plt

begin_tijd = time.time()

#Dit zijn alle settings. Deze kan je veranderen
lengte_van_reactor = 10**3
aantal_decimalen_tijd = 4
print_de_resulterende_lijst = 0
maxkental = 5
tijd_stappen = 100
start_neutron_aantal = 10**4
snelheid_rem = 1
start_uranium235_hoeveelheid = int((lengte_van_reactor ** 3) * 0.02)
muur_van_reactor_is_spiegel = True

start_uranium235_hoeveelheid = 10**3

toon_settings = True
if toon_settings:
 print('Deze zijn de settings:')
 print(f'lengte_van_reactor: {lengte_van_reactor}')
 print(f'maxkental: {maxkental}')
 print(f'tijd_stappen: {tijd_stappen}')
 print(f'start_neutron_aantal: {start_neutron_aantal}')
 print(f'start_uranium235_hoeveelheid: {start_uranium235_hoeveelheid}')
 print('')

#Dit zijn alle lists
list_neutron = []
list_uranium235 = []
aantal_neutronen_list = []
t_list = []

#Voegt neutronen toe aan de lijst
for _ in range(start_neutron_aantal):
 list_neutron.append([
 #Deze drie waardes zijn x,y,z coordinaten
 random.randint(1, lengte_van_reactor + 1),
 random.randint(1, lengte_van_reactor + 1),
 random.randint(1, lengte_van_reactor + 1),

 #Deze drie waardes zijn de snelheden in de x,y,z richting
 random.choice([random.randint(-maxkental,-1),random.randint(1,maxkental)]),
 random.choice([random.randint(-maxkental,-1),random.randint(1,maxkental)]),
 random.choice([random.randint(-maxkental,-1),random.randint(1,maxkental)])
])
#Hoogste x,y,z coordinaat is lengte_van_reactor + 1
#Laagste x,y,z coordinaat is 1
#Zo voorkom je deling door 0
print('Klaar met alle neutronen toevoegen')

for _ in range (start_uranium235_hoeveelheid):
 list_uranium235.append([
  #Deze drie waardes zijn x,y,z coordinaten
  random.randint(1, lengte_van_reactor + 1),
  random.randint(1, lengte_van_reactor + 1),
  random.randint(1, lengte_van_reactor + 1)
  ])

print('Klaar met alle U235 kernen toevoegen')
print('')

#Berekeningen

for t in range(tijd_stappen):
    
    print(f'Tijdstap {t} wordt behandeld')
    print(f'Er zijn nog {len(list_neutron)} neutronen over')
    print(f'Er zijn nog {len(list_uranium235)} uranium kernen over')
    #Dit is nodig om de grafieken te maken 
    aantal_neutronen_list.append(len(list_neutron))
    t_list.append(t)
    
    for neutron_index in range (len(list_neutron) - 1,-1,-1):
        list_neutron[neutron_index][0] += int(list_neutron[neutron_index][3]) * snelheid_rem   #Beweegt de neutron in de x-as
        list_neutron[neutron_index][1] += int(list_neutron[neutron_index][4]) * snelheid_rem   #Beweegt de neutron in de y-as
        list_neutron[neutron_index][2] += int(list_neutron[neutron_index][5]) * snelheid_rem   #Beweegt de neutron in de z-as
        
        #Beweging afgerond

        if muur_van_reactor_is_spiegel:
            #Reflectie van de neutronen met een te hoge coordinaat
            if (list_neutron[neutron_index][0] > lengte_van_reactor + 1):
             list_neutron[neutron_index][0] = 2 * (lengte_van_reactor + 1) - list_neutron[neutron_index][0]

            if (list_neutron[neutron_index][1] > lengte_van_reactor + 1):
             list_neutron[neutron_index][1] = 2 * (lengte_van_reactor + 1) - list_neutron[neutron_index][1]

            if (list_neutron[neutron_index][2] > lengte_van_reactor + 1):
             list_neutron[neutron_index][2] = 2 * (lengte_van_reactor + 1) - list_neutron[neutron_index][1]

            #Reflectie van de neutronen met een negatief coordinaat
            if (list_neutron[neutron_index][0] < 1):
             list_neutron[neutron_index][0] = 2-list_neutron[neutron_index][0]

            if (list_neutron[neutron_index][1] < 1):
             list_neutron[neutron_index][1] = 2-list_neutron[neutron_index][1]

            if (list_neutron[neutron_index][2] < 1):
             list_neutron[neutron_index][2] = 2-list_neutron[neutron_index][2]
        
        elif (list_neutron[neutron_index][0] > lengte_van_reactor or list_neutron[neutron_index][0] < 0 or
            list_neutron[neutron_index][1] > lengte_van_reactor or list_neutron[neutron_index][1] < 0 or
            list_neutron[neutron_index][2] > lengte_van_reactor or list_neutron[neutron_index][2] < 0
            ):
                list_neutron.pop(neutron_index)
                if toon_neutron_activiteit:
                 print('Neutron is uit de reactor gegaan')
                continue


        for uranium_index in range(len(list_uranium235) - 1, -1, -1):

            dx = list_uranium235[uranium_index][0] - list_neutron[neutron_index][0]
            dy = list_uranium235[uranium_index][1] - list_neutron[neutron_index][1]
            dz = list_uranium235[uranium_index][2] - list_neutron[neutron_index][2]

            
            if(int(dx/list_neutron[neutron_index][3]) ==
               int(dy/list_neutron[neutron_index][4]) ==
               int(dz/list_neutron[neutron_index][5])
               and 0<=dx/list_neutron[neutron_index][3]<=1
               and 0<=dy/list_neutron[neutron_index][4]<=1
               and 0<=dz/list_neutron[neutron_index][5]<=1
               ):

                 for herhaling in range(random.choice([2,3])):      #Voeg nieuwe neutronen toe
                     list_neutron.append([
                     list_neutron[neutron_index][0],
                     list_neutron[neutron_index][1],
                     list_neutron[neutron_index][2],
                     random.uniform(-maxkental, maxkental),
                     random.uniform(-maxkental, maxkental),
                     random.uniform(-maxkental, maxkental)
                 ])
                 del list_neutron[neutron_index]                 #Verwijder de oude neutronen en U235 kernen
                 del list_uranium235[uranium_index]
                 
                 break
    #if len(list_uranium235) == 0:
    #    print('Er zijn geen uranium kernen meer over')
    #    break

#Einde Berekeningen
print('Einde Berekeningen')

#resultaten printen
if print_de_resulterende_lijst:
    print(list_neutron)
    print()

print('Dit zijn alle resultaten:')
print('Er zijn nog ', len(list_neutron), 'neutronen over.')

#De tijd verstreken bereken en outputten:
tijd_verstreken = time.time() - begin_tijd
print(f'Tijd Verstreken: {round(time.time() - begin_tijd, aantal_decimalen_tijd)} s')
print(f'Er zijn {tijd_stappen} tijdstappen verstreken.')
print(f'Je hebt {round((lengte_van_reactor * 3) * 238.02891 / (10 ** 23) / 6.02214076 / 19050000, 4)} m^3 uranium gemodelleerd.')


#Grafieken maken


plt.plot(t_list, aantal_neutronen_list)
plt.xlabel('Tijd')
plt.ylabel('Aantal Neutronen')
plt.title('Aantal Neutronen per Tijdseenheid')
plt.xlim(0, max(t_list)*1.2)
plt.ylim(0, max(aantal_neutronen_list)*1.2)
plt.show()
#Einde Grafieken maken

#Voeg toe aan de reactor: Water, Xenon135, Staven, Uranium 235
#Einde