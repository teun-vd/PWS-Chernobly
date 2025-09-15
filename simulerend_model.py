#Import alle modules
import random
import math
import time
import matplotlib.pyplot as plt

#Dit is o
begin_tijd = time.time()

#Variabelen
aantal_decimalen_tijd = 2
print_de_resulterende_lijst = 0
maxkental = 5
totaal_aantal_botsingen = 0

#Settings. Deze kan je veranderen
kans_op_Xenon135_ontstaat = 0.1
kans_op_nieuwe_neutron_ontstaat = 0.0
#Minder Belangrijke Settings
toon_settings = True
tijd_stappen = 10000

doel_neutron_aantal = 10000000000

lengte_van_reactor = int(10**2) #Lengte van een zijde van de reactor in U-kernen. Er zijn dus lengte_van_reactor^3 U-kernen in de reactor
start_neutron_aantal = int(100)
kans_op_nieuwe_neutron_ontstaat = 0.05
start_uranium235_hoeveelheid = int((lengte_van_reactor ** 3) * 0.02)
if toon_settings:
    print('Dit zijn de settings:')
    print(f'lengte_van_reactor: {lengte_van_reactor}')
    print(f'maxkental: {maxkental}')
    print(f'tijd_stappen: {tijd_stappen}')
    print(f'start_neutron_aantal: {start_neutron_aantal}')
    print(f'doel_neutron_aantal: {doel_neutron_aantal}')
    print(f'start_uranium235_hoeveelheid: {start_uranium235_hoeveelheid}')
    print('')

#Dit zijn alle lijsten
lijst_neutron = []
lijst_uranium235 = []
lijst_Xenon135 = []
aantal_neutronen_lijst = []
aantal_xenon135_lijst = []
lijst_van_tijden = []
lijst_q = []
lijst_p = []
lijst_doel_neutron_aantal = []


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
        #kwadraat_snelheid = lijst_neutron[neutron_index][7] 
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
    #lijst_met_potentiele_botsingen bevat nu alleen botsingen met d<1
    #Nu splitsen we deze lijst in twee: botsingen met t<0 en t>0
    lijst_met_botsingen_t_negatief = []
    lijst_met_botsingen_t_positief = []
    for potentiele_botsing_index in range(len(lijst_met_potentiele_botsingen)-1,-1,-1):
        if lijst_met_potentiele_botsingen[potentiele_botsing_index][1] < 0:
            lijst_met_botsingen_t_negatief.append(lijst_met_potentiele_botsingen[potentiele_botsing_index])

        if lijst_met_potentiele_botsingen[potentiele_botsing_index][1] >= 0:
            lijst_met_botsingen_t_positief.append(lijst_met_potentiele_botsingen[potentiele_botsing_index])

    #Nu sorteren we de lijst_met_botsingen_t_positief op t
    lijst_met_botsingen_t_positief.sort(key=lambda x: x[1])

    #Nu sorteren we de lijst_met_botsingen_t_negatief op t
    lijst_met_botsingen_t_negatief.sort(key=lambda x: x[1], reverse=True)
    
    #Nu selecteren we de botsing met de kortste tijd. Deze bosting zal als eerst gebeuren
    
    if len(lijst_met_botsingen_t_positief) == 0 and len(lijst_met_botsingen_t_negatief) == 0:
        minimale_positieve_t = None
        object_met_minimale_afstand_in_toekomst = None
        minimale_negatieve_t = None
        object_met_minimale_afstand_in_verleden = None
    elif len(lijst_met_botsingen_t_positief) == 0:
        minimale_positieve_t = None
        object_met_minimale_afstand_in_toekomst = None
        minimale_negatieve_t = lijst_met_botsingen_t_negatief[0][1] 
        object_met_minimale_afstand_in_verleden = lijst_met_botsingen_t_negatief[0][2]
    elif len(lijst_met_botsingen_t_negatief) == 0:
        minimale_positieve_t = lijst_met_botsingen_t_positief[0][1] 
        object_met_minimale_afstand_in_toekomst = lijst_met_botsingen_t_positief[0][2]
        minimale_negatieve_t = None
        object_met_minimale_afstand_in_verleden = None
    elif not len(lijst_met_botsingen_t_positief) == 0 and not len(lijst_met_botsingen_t_negatief) == 0:
        minimale_positieve_t = lijst_met_botsingen_t_positief[0][1] 
        object_met_minimale_afstand_in_toekomst = lijst_met_botsingen_t_positief[0][2]
        minimale_negatieve_t = lijst_met_botsingen_t_negatief[0][1] 
        object_met_minimale_afstand_in_verleden = lijst_met_botsingen_t_negatief[0][2]
    
    return minimale_positieve_t, object_met_minimale_afstand_in_toekomst, minimale_negatieve_t, object_met_minimale_afstand_in_verleden

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
    0
    #Hoe lang staat deze neutron in 'slaapstand'
    #0 betekent dat de neutron direct behandeld moet worden
    ])
    #De kwadraat van de snelheid van deze neutron is belangrijk voor de botsingen. Daarom berekenen we deze alvast.
    #lijst_neutron[object_index].append(lijst_neutron[object_index][3] ** 2 + lijst_neutron[object_index][4] ** 2 + lijst_neutron[object_index][5] ** 2)
print('Klaar met alle neutronen toevoegen')
#Yapverhaal
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
aantal_neutronen_lijst_verschil = []
#Hier start de daadwerkelijke simulatie
for tijd in range(tijd_stappen):  

    #Informatie Printen  
    print(f'Tijdstap {tijd} wordt behandeld')
    print('')
    
    #Dit is nodig om de grafieken te maken 
    aantal_neutronen_lijst.append(len(lijst_neutron))
    aantal_xenon135_lijst.append(len(lijst_Xenon135))
    lijst_van_tijden.append(tijd)
    aantal_neutronen_lijst_verschil.append(len(lijst_neutron) - aantal_neutronen_lijst[tijd-1] if tijd > 0 else len(lijst_neutron))
    lijst_doel_neutron_aantal.append(doel_neutron_aantal)
    
    q = (len(lijst_neutron) - doel_neutron_aantal)/doel_neutron_aantal
    #Oude formules voor P(Q), worden hier niet gebruikt
    #p = -1 * math.log((q + 0.01),2) if (q + 0.01) > 0 else 0
    #p = 1 - (q + 0.01) 
    #p = 2 * q
    #p = math.exp(q) - 1,
    #p = -100 * x
    #p = 1 * q + 0.1
    #p = 0.5/(1 + math.exp(1.5 - 5 * q))
    
    p = 70 * q ** 3 + 0.072
    if p > 0.5:
        p = 0.5    
    if p < 0:
        p = 0
    
    lijst_q.append(q)  
    lijst_p.append(p)  
    
    #Elke neutron behandelen
    for neutron_index in range (len(lijst_neutron) - 1,-1,-1):
        
        if p > random.random():
            del lijst_neutron[neutron_index]
            continue
            
        if lijst_neutron[neutron_index][6] == 0:
            #Deze neutron staat dus niet in slaapstand. Daarom behandelen we deze neutron voor botsingen met uranium235 kernen
            minimale_positieve_t, object_met_minimale_afstand_in_toekomst, _, _ = (
            afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_uranium235))
            
            if minimale_positieve_t is None:
                lijst_neutron[neutron_index][6] = 2^32
                '''
                De neutron zal voorlopig niet botsen. We behandelen deze voorlopig niet meer, tot deze reflecteert. 
                Dan verandert de lijn waarop de neiutron beweegt, en kan de nuetron dus botsen met andere kernen
                '''

            elif 0 <= minimale_positieve_t <= 1:
                totaal_aantal_botsingen += 1
                #Deze neutron botst met een uranium235 kern
                for _ in range(random.choice([2,3])):      #Voeg nieuwe neutronen toe.
                    lijst_neutron.append([
                                lijst_neutron[neutron_index][0],
                                lijst_neutron[neutron_index][1],
                                lijst_neutron[neutron_index][2],
                                random.uniform(-maxkental, maxkental),
                                random.uniform(-maxkental, maxkental),
                                random.uniform(-maxkental, maxkental),
                                0])
                    #lijst_neutron[len(lijst_neutron) - 1].append(lijst_neutron[neutron_index][3] ** 2 + lijst_neutron[neutron_index][4] ** 2 + lijst_neutron[neutron_index][5] ** 2)
                lijst_uranium235.append([
                random.randint(1, lengte_van_reactor + 1),
                random.randint(1, lengte_van_reactor + 1),
                random.randint(1, lengte_van_reactor + 1)])
                #Voeg Xenon135 toe
                if random.random() < kans_op_Xenon135_ontstaat:
                    lijst_Xenon135.append(lijst_uranium235[object_met_minimale_afstand_in_toekomst])
     
                #Verwijder de oude neutronen en U235 kernen
                del lijst_neutron[neutron_index] 
                del lijst_uranium235[object_met_minimale_afstand_in_toekomst]

                continue
            
            elif minimale_positieve_t > 1:
                #De neutron zal pas later botsen. We hoeven deze neutron dus niet te behandelen voor de volgende (t-1) tijdstappen
                #Deze neutron gaat dus in een soort slaapstand voor t-1 tijdstappen
                lijst_neutron[neutron_index][6] = math.ceil(minimale_positieve_t-1)
                #print(f'Neutron {neutron_index} gaat in slaapstand voor {math.ceil(minimale_positieve_t-1)} tijdstappen')
        else:
            #Deze neutron staat in slaapstand. We moeten deze neutron dus niet behandelen voor botsingen met uranium235 kernen
            lijst_neutron[neutron_index][6] += -1

        #We hebben gecheckt voor potentiele botsingen met U235. Nu doen we hetzelfde met X135
        minimale_positieve_t, object_met_minimale_afstand_in_toekomst, _, _ = (
        afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_Xenon135))
        if minimale_positieve_t is None:
            pass
        elif minimale_positieve_t < 1:
            #De neutron botst met Xenon135
            totaal_aantal_botsingen += 1
            del lijst_Xenon135[object_met_minimale_afstand_in_toekomst]
            del lijst_neutron[neutron_index]
            break

        #Nu gaan de neutronen bewegen.
        lijst_neutron[neutron_index][0] += int(lijst_neutron[neutron_index][3])   #Beweegt de neutron in de x-as
        lijst_neutron[neutron_index][1] += int(lijst_neutron[neutron_index][4])   #Beweegt de neutron in de y-as
        lijst_neutron[neutron_index][2] += int(lijst_neutron[neutron_index][5])   #Beweegt de neutron in de z-as
#De neutronen reflecteren
#De neutronen reflecteren niet echt, 
#ze gaan gewoon naar de andere kant van de reactor. 
#De muren van de reactor zijn geen spiegels, 
#maar portalen naar de andere kant van de reactor.
#De reactor is geen ruimte zoals in pong, maar een ruimte zoals in pacman
   


        is_de_neutron_gereflecteerd = False
        if  lijst_neutron[neutron_index][0] > lengte_van_reactor:
            lijst_neutron[neutron_index][0] += -lengte_van_reactor
            is_de_neutron_gereflecteerd = True

        if  lijst_neutron[neutron_index][1] > lengte_van_reactor:
            lijst_neutron[neutron_index][1] += -lengte_van_reactor
            is_de_neutron_gereflecteerd = True

        if  lijst_neutron[neutron_index][2] > lengte_van_reactor:
            lijst_neutron[neutron_index][2] += -lengte_van_reactor
            is_de_neutron_gereflecteerd = True

        if  lijst_neutron[neutron_index][0] < 1:
            lijst_neutron[neutron_index][0] += lengte_van_reactor
            is_de_neutron_gereflecteerd = True

        if  lijst_neutron[neutron_index][1] < 1:
            lijst_neutron[neutron_index][1] += lengte_van_reactor
            is_de_neutron_gereflecteerd = True

        if  lijst_neutron[neutron_index][2] < 1:
            lijst_neutron[neutron_index][2] += lengte_van_reactor
            is_de_neutron_gereflecteerd = True

        if is_de_neutron_gereflecteerd:
            lijst_neutron[neutron_index][6] = 0
            _, _, minimale_negatieve_t, object_met_minimale_afstand_in_verleden = (
                afstand_punt_tot_vector(lijst_neutron, neutron_index, lijst_uranium235))
            if minimale_negatieve_t is not None and -1 < minimale_negatieve_t < 0:
                for _ in range(random.choice([2,3])):      #Voeg nieuwe neutronen toe.
                    lijst_neutron.append([
                        lijst_neutron[neutron_index][0],
                        lijst_neutron[neutron_index][1],
                        lijst_neutron[neutron_index][2],
                        random.uniform(-maxkental, maxkental),
                        random.uniform(-maxkental, maxkental),
                        random.uniform(-maxkental, maxkental),
                        0])
                    #lijst_neutron[len(lijst_neutron) - 1].append(lijst_neutron[neutron_index][3] ** 2 + lijst_neutron[neutron_index][4] ** 2 + lijst_neutron[neutron_index][5] ** 2)

                lijst_uranium235.append([                  #Voeg nieuwe U235 kernen toe
                    random.randint(1, lengte_van_reactor + 1),
                    random.randint(1, lengte_van_reactor + 1),
                    random.randint(1, lengte_van_reactor + 1)
                ])
                    
                
                #Voeg Xenon135 toe
                if random.random() < kans_op_Xenon135_ontstaat:
                    lijst_Xenon135.append(lijst_uranium235[object_met_minimale_afstand_in_verleden])

                #Verwijder de oude neutronen en U235 kernen
                del lijst_neutron[neutron_index]
                del lijst_uranium235[object_met_minimale_afstand_in_verleden]




    #Deze tijdstip if afgelopen
    #print(f'Er zijn {len(lijst_uranium235)} uranium kernen ')
    print(f'Er zijn {len(lijst_Xenon135)} Xenon135 kernen ')
    print(f'Er zijn {len(lijst_neutron)} neutronen ')

    #Uraniumkeren regeneren, dus dit zal nooit voorkomen. Overblijfsel van vorige versies.
    if len(lijst_uranium235) == 0:
        #De simulatie is dus afgelopen
        print('')
        print('Er zijn geen uranium kernen meer over')
        break
    
#Einde Berekeningen
print('Einde Simulatie')

#Resultaten printen
print('Dit zijn alle resultaten:')

m3 = (lengte_van_reactor * 3) * 238.02891 / (10 ** 23) / 6.02214076 / 10970000
cm3 = m3 * 10**6
mm3= cm3 * 1000
print(f'Je hebt {round(mm3, 4)} mm^3 uranium gemodelleerd')
print(f'Je hebt {m3} m^3 uranium gemodelleerd')
print(f'Je hebt {round((lengte_van_reactor * 3) * 238.02891 / (10 ** 23) / 6.02214076 / 10970000, 4)} m^3 uranium gemodelleerd.')
print(f'Je hebt {round((lengte_van_reactor * 3) * 238.02891 / (10 ** 23) / 6.02214076 / 10970000 * 238.02891, 4)} kg uranium gemodelleerd.')

#De tijd verstreken bereken en outputten:
tijd_verstreken = time.time() - begin_tijd
print(f'Tijd Verstreken: {round(time.time() - begin_tijd, aantal_decimalen_tijd)} s')

energie_vrijgekomen_in_MeV = totaal_aantal_botsingen * 202.5
energie_vrijgekomen_in_GeV = energie_vrijgekomen_in_MeV * 1000
energie_vrijgekomen_in_J = energie_vrijgekomen_in_GeV * 1.602176634 * 10**(-10)

print(f'Er zijn {totaal_aantal_botsingen} botsingen geweest.')
print(f'Er is {energie_vrijgekomen_in_GeV} GeV aan energie vrij gekomen')
print(f'Er is {energie_vrijgekomen_in_J} J aan energie vrij gekomen')
print(f'Je hebt {start_uranium235_hoeveelheid} uranium235 kernen gemodelleerd')
print(f'In een hele RBMK1000 reactor zou {(765 / m3) * energie_vrijgekomen_in_J} J aan energie vrijkomen')
print(f'De gemiddelde waarde van q was {round(sum(lijst_q)/len(lijst_q), 4)}')
print(f'De gemiddelde aantan Xe135 kernen was {round(sum(aantal_xenon135_lijst)/len(aantal_xenon135_lijst), 4)}')
#Grafieken maken
if True: #Grafiekjes maken
    plt.plot(lijst_van_tijden, aantal_neutronen_lijst)
    plt.axhline(y=doel_neutron_aantal, color='red', linewidth=3, linestyle='-', label='Doel Neutron Aantal')
    plt.xlabel('Tijd')
    plt.ylabel('Aantal Neutronen')
    plt.title('Aantal Neutronen per Tijdseenheid')
    plt.xlim(0, max(lijst_van_tijden))
    if max(aantal_neutronen_lijst) > doel_neutron_aantal:
        plt.ylim(0, max(aantal_neutronen_lijst) * 1.05)
    else:
        plt.ylim(0, doel_neutron_aantal * 1.05)
    plt.show()


    plt.plot(lijst_van_tijden, aantal_neutronen_lijst, '-', linewidth=1)  # Solid line
    plt.axhline(y=doel_neutron_aantal, color='red', linewidth=3, linestyle='-', label='Doel Neutron Aantal')
    plt.xlabel('Tijd')
    plt.ylabel('Aantal Neutronen')
    plt.title('Aantal Neutronen per Tijdseenheid')
    plt.xlim(0, max(lijst_van_tijden))
    if max(aantal_neutronen_lijst) > doel_neutron_aantal:
        plt.ylim(0, max(aantal_neutronen_lijst) * 1.05)
    else:
        plt.ylim(0, doel_neutron_aantal * 1.05)
    plt.show()
    
    
    skip = 5  # Adjust based on your needs
    plt.plot(lijst_van_tijden[::skip], aantal_neutronen_lijst[::skip], '-')
    plt.axhline(y=doel_neutron_aantal, color='red', linewidth=3, linestyle='-', label='Doel Neutron Aantal')
    plt.xlabel('Tijd')
    plt.ylabel('Aantal Neutronen')
    plt.title('Aantal Neutronen per Tijdseenheid')
    plt.xlim(0, max(lijst_van_tijden))
    if max(aantal_neutronen_lijst) > doel_neutron_aantal:
        plt.ylim(0, max(aantal_neutronen_lijst) * 1.05)
    else:
        plt.ylim(0, doel_neutron_aantal * 1.05)
    plt.show()

    plt.plot(aantal_neutronen_lijst, aantal_xenon135_lijst, '.', markersize=2)  # Faster than scatterplt.xlabel('Tijd')
    plt.ylabel('Aantal Xenon135 Kernen')
    plt.title('Aantal Xenon135 Kernen per Tijdseenheid')
    plt.xlim(0, max(lijst_van_tijden))
    plt.ylim(0, max(aantal_xenon135_lijst))
    plt.show()

    plt.scatter(aantal_neutronen_lijst, aantal_xenon135_lijst)
    plt.xlabel('Aantal Neutronen')
    plt.ylabel('Aantal Xenon135 Kernen')
    plt.title('Aantal Neutronen vs Aantal Xenon135 Kernen')
    plt.xlim(0, max(aantal_neutronen_lijst))
    plt.ylim(0, max(aantal_xenon135_lijst))
    plt.show()
    
    plt.plot(lijst_van_tijden, lijst_p)
    plt.xlabel('Tijd')
    plt.ylabel('P(Q)')
    plt.title('P(Q) per Tijdseenheid')
    plt.xlim(0, max(lijst_van_tijden))
    plt.ylim(0, max(lijst_p))
    plt.show()