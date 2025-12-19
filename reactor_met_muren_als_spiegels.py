#Import alle modules
import random
import math
import time
import matplotlib.pyplot as plt

begin_tijd = time.time()

#Variabelen
aantal_decimalen_tijd = 2
print_de_resulterende_lijst = 0
maxkental = 5
totaal_aantal_botsingen = 0

#Settings. Deze kan je veranderen
#lengte_van_reactor = 10**3
#start_neutron_aantal = 10**4
#start_uranium235_hoeveelheid = 10**3
#kans_op_nieuwe_neutron_ontstaat = 0.0

#Minder Belangrijke Settings
toon_settings = True
tijd_stappen = 100
#start_uranium235_hoeveelheid = int((lengte_van_reactor ** 3) * 0.02)

lengte_van_reactor = int(10**3)
start_neutron_aantal = int(10**2)
start_uranium235_hoeveelheid = int(10**4)
kans_op_nieuwe_neutron_ontstaat = 0
kans_op_Xenon135_ontstaat = 0.3


if toon_settings:
    print('Dit zijn de settings:')
    print(f'lengte_van_reactor: {lengte_van_reactor}')
    print(f'maxkental: {maxkental}')
    print(f'tijd_stappen: {tijd_stappen}')
    print(f'start_neutron_aantal: {start_neutron_aantal}')
    print(f'start_uranium235_hoeveelheid: {start_uranium235_hoeveelheid}')
    print('')

#Dit zijn alle lijsten
lijst_neutron = []
lijst_uranium235 = []
lijst_Xenon135 = []
aantal_neutronen_lijst = []
lijst_van_tijden = []

#Functie defineren
def afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_die_gecheckt_wordt):
    
    xvector = lijst_neutron[neutron_index][3]
    yvector = lijst_neutron[neutron_index][4]
    zvector = lijst_neutron[neutron_index][5]
    
    lijst_met_potentiele_botsingen = []
    for object_index in range(len(lijst_die_gecheckt_wordt)):
        
        xpunt = lijst_neutron[neutron_index][0] - lijst_die_gecheckt_wordt[object_index][0]
        ypunt = lijst_neutron[neutron_index][1] - lijst_die_gecheckt_wordt[object_index][1]
        zpunt = lijst_neutron[neutron_index][2] - lijst_die_gecheckt_wordt[object_index][2]
        
        kwadraat_snelheid = xvector ** 2 + yvector ** 2 + zvector ** 2
        kwadaat_afstand_punt_tot_oorsprong = xpunt**2 + ypunt**2 + zpunt**2
        inproduct = xvector * xpunt + yvector * ypunt + zvector * zpunt
        
        #Zie voor verantwoording van onderstaande formule het document waarin de simulatie is uitgelegd
        afstand_kwadraat = (
            kwadaat_afstand_punt_tot_oorsprong - (
            inproduct ** 2 / kwadraat_snelheid
            ))
        t = (xpunt * xvector + ypunt * yvector + zpunt * zvector)/(kwadraat_snelheid)
        
        if afstand_kwadraat < 1:
           lijst_met_potentiele_botsingen.append([afstand_kwadraat, t, object_index]) 
        
        for potentiele_botsing_index in range(len(lijst_met_potentiele_botsingen)-1,-1,-1):
            afstand_kwadraat, t, object_index = lijst_met_potentiele_botsingen[potentiele_botsing_index]
            
            if not afstand_kwadraat < 1:
                #Deze botsing is niet mogelijk
                del lijst_met_potentiele_botsingen[potentiele_botsing_index]
                continue

    #De lijst_met_potentiele_botsingen bevat nu alleen botsingen met d<1
    #Nu moeten we nog sorteren op t, zodat we de botsing met de kortste tijd eerst hebben
    
    minimale_positive_t = 1000000000000000000
    minimale_negatieve_t = -10000000000000000
    object_met_minimale_afstand_in_toekomst = None
    object_met_minimale_afstand_in_verleden = None
    
    for potentiele_botsing_index in range(len(lijst_met_potentiele_botsingen)-1,-1,-1):
        if 0 < lijst_met_potentiele_botsingen[potentiele_botsing_index][1] < minimale_positive_t:
            minimale_positive_t = lijst_met_potentiele_botsingen[potentiele_botsing_index][1]
            object_met_minimale_afstand_in_toekomst = lijst_met_potentiele_botsingen[potentiele_botsing_index][2]
        
        if -1 < lijst_met_potentiele_botsingen[potentiele_botsing_index][1] < minimale_negatieve_t and lijst_met_potentiele_botsingen[potentiele_botsing_index][1] < 0:
            minimale_negatieve_t = lijst_met_potentiele_botsingen[potentiele_botsing_index][1]
            object_met_minimale_afstand_in_verleden = lijst_met_potentiele_botsingen[potentiele_botsing_index][2]
        '''
        We hebben nu de twee 'beste' botsingen gevonden.
        Het kan dat er geen btosingen worden gevonden. Dan gelden nog steeds de initiële waardes
        voor t en zijn de objecten None'''
    return minimale_positive_t, object_met_minimale_afstand_in_toekomst, minimale_negatieve_t, object_met_minimale_afstand_in_verleden

def check_voor_neutron_botsting_in_verleden(neutron_index, lijst_neutron, lijst_uranium235):            
    _, _, Minimale_negatieve_t, object_met_minimale_afstand_in_verleden = (
    afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_uranium235))
    if Minimale_negatieve_t < 0 and not object_met_minimale_afstand_in_verleden is None:
        #De neutron is dus gebotst met een U235 kern
        
        #Fissie vindt plaats
        for _ in range(random.choice([2,3])):      #Voeg nieuwe neutronen toe. Zie voor die stuk r120-140
            lijst_neutron.append([
            lijst_neutron[neutron_index][0],
            lijst_neutron[neutron_index][1],
            lijst_neutron[neutron_index][2],
            random.uniform(-maxkental, maxkental),
            random.uniform(-maxkental, maxkental),
            random.uniform(-maxkental, maxkental),
            0])  
            #Voeg Xenon135 toe
            if random.random() < kans_op_Xenon135_ontstaat:
                lijst_Xenon135.append(lijst_uranium235[object_met_minimale_afstand_in_verleden])
                
            #Verwijder de oude neutronen en U235 kernen
            del lijst_neutron[neutron_index] 
            del lijst_uranium235[object_met_minimale_afstand_in_verleden]
            break


#Voegt neutronen toe aan de lijst
for object_index in range(start_neutron_aantal):
    lijst_neutron.append([
    #Deze drie waardes zijn x,y,z coordinaten
    random.randint(1, lengte_van_reactor + 1),
    random.randint(1, lengte_van_reactor + 1),
    random.randint(1, lengte_van_reactor + 1),

    #Deze drie waardes zijn de snelheden in de x,y,z richting
    random.choice([random.randint(-maxkental,-1),random.randint(1,maxkental)]),
    random.choice([random.randint(-maxkental,-1),random.randint(1,maxkental)]),
    random.choice([random.randint(-maxkental,-1),random.randint(1,maxkental)]),
    
    #Hoe lang staat deze neutron in 'slaapstand'
    0  #0 betekent dat de neutron direct behandeld moet worden
])
print('Klaar met alle neutronen toevoegen')
'''
Hoogste x,y,z coordinaat is lengte_van_reactor + 1
Laagste x,y,z coordinaat is 1
Zo voorkom je deling door 0
'''

#Voegt uranium235 kernen toe aan de lijst
for object_index in range (start_uranium235_hoeveelheid):
    lijst_uranium235.append([
    #Deze drie waardes zijn x,y,z coordinaten
    random.randint(1, lengte_van_reactor + 1),
    random.randint(1, lengte_van_reactor + 1),
    random.randint(1, lengte_van_reactor + 1)
    #Uranium beweegt niet dus vandaar geen bewegingsvector
    ])

print('Klaar met alle U235 kernen toevoegen')
print('')

#Hier start de daadwerkelijke simulatie
for tijd in range(tijd_stappen):  

    #Informatie Printen  
    print(f'Tijdstap {tijd} wordt behandeld')
    
    print('')
    #Dit is nodig om de grafieken te maken 
    aantal_neutronen_lijst.append(len(lijst_neutron))
    lijst_van_tijden.append(tijd)
    
    #Elke neutron behandelen
    for neutron_index in range (len(lijst_neutron) - 1,-1,-1):
        if lijst_neutron[neutron_index][6] == 0:
            #Deze neutron staat dus niet in slaapstand. Daarom behandelen we deze neutron voor botsingen met uranium235 kernen
            minimale_positive_t, object_met_minimale_afstand_in_toekomst, _, _ = (
            afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_uranium235))

            if minimale_positive_t < 1 and minimale_positive_t > 0 and not object_met_minimale_afstand_in_toekomst is None:
                totaal_aantal_botsingen += 1

                #Fissie vindt plaats
                for herhaling in range(random.choice([2,3])):      #Voeg nieuwe neutronen toe. Zie voor die stuk r120-140
                    lijst_neutron.append([
                    lijst_neutron[neutron_index][0],
                    lijst_neutron[neutron_index][1],
                    lijst_neutron[neutron_index][2],
                    random.uniform(-maxkental, maxkental),
                    random.uniform(-maxkental, maxkental),
                    random.uniform(-maxkental, maxkental),
                    0])  
                    
                    #Voeg Xenon135 toe
                if random.random() < kans_op_Xenon135_ontstaat:
                    lijst_Xenon135.append(lijst_uranium235[object_met_minimale_afstand_in_toekomst])
                    
                #Verwijder de oude neutronen en U235 kernen
                del lijst_neutron[neutron_index] 
                del lijst_uranium235[object_met_minimale_afstand_in_toekomst]
                break
            
            elif minimale_positive_t > 1 and minimale_positive_t < 10000000:
                #De neutron zal pas later botsen. We hoeven deze neutron dus niet te behandelen voor de volgende (t-1) tijdstappen
                #Deze neutron gaat dus in een soort slaapstand over t-1 tijdstappen
                lijst_neutron[neutron_index][6] = math.ceil(minimale_positive_t-1)
                #print(f'Neutron {neutron_index} gaat in slaapstand voor {math.ceil(minimale_positive_t-1)} tijdstappen') 
        else:
            #Deze neutron staat in slaapstand. We moeten deze neutron dus niet behandelen voor botsingen met uranium235 kernen
            lijst_neutron[neutron_index][6] += -1

        #We hebben gecheckt voor potentiele botsingen met U235. Nu doen we hetzelfde met X135
        minimale_positive_t, object_met_minimale_afstand_in_toekomst, _, _ = (
        afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_Xenon135))
        if minimale_positive_t < 1:
            #De neutron botst met Xenon135
            totaal_aantal_botsingen += 1
            del lijst_Xenon135[object_met_minimale_afstand_in_toekomst]
            del lijst_neutron[neutron_index]
            break
            
        #Nu gaan de neutronen bewegen.
        lijst_neutron[neutron_index][0] += int(lijst_neutron[neutron_index][3])   #Beweegt de neutron in de x-as
        lijst_neutron[neutron_index][1] += int(lijst_neutron[neutron_index][4])   #Beweegt de neutron in de y-as
        lijst_neutron[neutron_index][2] += int(lijst_neutron[neutron_index][5])   #Beweegt de neutron in de z-as   
        is_de_neutron_gereflecteerd = False
        
        #De neutronen reflecteren
        if  lijst_neutron[neutron_index][0] > lengte_van_reactor:
            lijst_neutron[neutron_index][0] += -lengte_van_reactor
            _, _, Minimale_negatieve_t, object_met_minimale_afstand_in_verleden = (
            afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_uranium235))
            if Minimale_negatieve_t < 0:
                totaal_aantal_botsingen += 1
                check_voor_neutron_botsting_in_verleden(neutron_index, lijst_neutron, lijst_uranium235)
        
        if  lijst_neutron[neutron_index][1] > lengte_van_reactor:
            lijst_neutron[neutron_index][1] += -lengte_van_reactor
            _, _, Minimale_negatieve_t, object_met_minimale_afstand_in_verleden = (
            afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_uranium235))
            if Minimale_negatieve_t < 0:
                totaal_aantal_botsingen += 1
                check_voor_neutron_botsting_in_verleden(neutron_index, lijst_neutron, lijst_uranium235)
                
        if  lijst_neutron[neutron_index][2] > lengte_van_reactor:
            lijst_neutron[neutron_index][2] += -lengte_van_reactor
            _, _, Minimale_negatieve_t, object_met_minimale_afstand_in_verleden = (
            afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_uranium235))
            if Minimale_negatieve_t < 0:
                totaal_aantal_botsingen += 1
                check_voor_neutron_botsting_in_verleden(neutron_index, lijst_neutron, lijst_uranium235)
                
        if  lijst_neutron[neutron_index][0] < 1:
            lijst_neutron[neutron_index][0] += lengte_van_reactor
            _, _, Minimale_negatieve_t, object_met_minimale_afstand_in_verleden = (
                afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_uranium235))
            if Minimale_negatieve_t < 0:
                totaal_aantal_botsingen += 1
                check_voor_neutron_botsting_in_verleden(neutron_index, lijst_neutron, lijst_uranium235)
                
        if  lijst_neutron[neutron_index][1] < 1:
            lijst_neutron[neutron_index][1] += lengte_van_reactor
            _, _, Minimale_negatieve_t, object_met_minimale_afstand_in_verleden = (
                afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_uranium235))
            if Minimale_negatieve_t < 0:
                totaal_aantal_botsingen += 1
                check_voor_neutron_botsting_in_verleden(neutron_index, lijst_neutron, lijst_uranium235)
                
        if  lijst_neutron[neutron_index][2] < 1:
            lijst_neutron[neutron_index][2] += lengte_van_reactor
            _, _, Minimale_negatieve_t, object_met_minimale_afstand_in_verleden = (
                afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_uranium235))
            if Minimale_negatieve_t < 0:
                totaal_aantal_botsingen += 1
                check_voor_neutron_botsting_in_verleden(neutron_index, lijst_neutron, lijst_uranium235)
    
    #Deze tijdstip if afgelopen
    print(f'Er zijn {len(lijst_uranium235)} uranium kernen ')
    print(f'Er zijn {len(lijst_Xenon135)} Xenon135 kernen ')
    print(f'Er zijn {len(lijst_neutron)} neutronen ')

    if len(lijst_uranium235) == 0:
        #De simulatie is dus afgelopen
        print('')
        print('Er zijn geen uranium kernen meer over')
        break
    
#Einde Berekeningen
print('Einde Simulatie')

#Resultaten printen
print('Dit zijn alle resultaten:')

print(f'Je hebt {round((lengte_van_reactor * 3) * 238.02891 / (10 ** 23) / 6.02214076 / 19050000, 4)} m^3 uranium gemodelleerd.')
print(f'Je hebt {round((lengte_van_reactor * 3) * 238.02891 / (10 ** 23) / 6.02214076 / 19050000 * 238.02891, 4)} kg uranium gemodelleerd.')

#De tijd verstreken bereken en outputten:
tijd_verstreken = time.time() - begin_tijd
print(f'Tijd Verstreken: {round(time.time() - begin_tijd, aantal_decimalen_tijd)} s')

energie_vrijgekomen_in_MeV = totaal_aantal_botsingen * 202.5
print(f'Er zijn {totaal_aantal_botsingen} botsingen geweest.')
print(f'Er is {energie_vrijgekomen_in_MeV} MeV aan energie vrij gekomen')
#print(f'Er is {energie_vrijgekomen_in_MeV * 1.602176634 * 10**(-13) / 10**6} J aan energie vrij gekomen')

#Grafieken maken
plt.plot(lijst_van_tijden, aantal_neutronen_lijst)
plt.xlabel('Tijd')
plt.ylabel('Aantal Neutronen')
plt.title('Aantal Neutronen per Tijdseenheid')
plt.xlim(0, max(lijst_van_tijden)*1.2)
plt.ylim(0, max(aantal_neutronen_lijst)*1.2)
plt.show()

#Voeg toe aan de reactor: Water, Staven
#zorgt dat de randen van de reactor 'spiegels' zijn. dus de neutronen spiegelen en stuiteren terug als ze de randen raken