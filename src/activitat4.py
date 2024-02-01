import time

import copy
import random

nom_grups = {'1':'cientific', '2':'tecnologic', '3':'humanistic', '4':'artistic'}
nom_optatives = {'1':'informatica', '2':'llati', '3':'teatre', '4':'frances'}
violacions_puntuacio = {'lleu':10 ** 0, 'greu':10 ** 1, 'molt greu':10 ** 3}
places_grup = {'1':20, '2':20, '3':30, '4':30}
places_optativa = {'1':25, '2':25, '3':25, '4':25}
num_poblacions = 20
num_generacions = 100
pecentatge_progenitors = 0.5

def llegir_preferencies_alumnes(nom_fitxer):
    lines = [(l.strip()).split(",") for l in (open(nom_fitxer).readlines())]
    alumnes = {}
    for args in lines:
        preferencies_grup = {}
        preferencies_grup = {'primer_grup':args[1], 'segon_grup':args[2]}
        preferencies_optativa = {}
        preferencies_optativa = {'primera_optativa':args[3], 'segona_optativa':args[4], 'tercera_optativa':args[5]}
        alumnes[int(args[0])] = [preferencies_grup, preferencies_optativa, args[6] == 's']
    return alumnes

def mostar_preferencies_alumnes(alumnes):
    print ''
    print '[id][' + '1er gruo'.ljust(10) + '][' + '2on grup'.ljust(10) + '][' + '1ra opt.'.ljust(11) + '][' + '2na opt.'.ljust(11) + '][' + '3ra opt.'.ljust(11) + '][' + 'FR3 ?'.ljust(5) + ']'
    print ' --  ----------  ----------  -----------  -----------  -----------  -----'
    for k, v in alumnes.items():
        preferencies_grup = v[0]
        preferencies_optativa = v[1]
        frances_tercer = v[2]
        linia = '[' + str(k).rjust(2) + ']'
        linia += '[' + str(nom_grups[preferencies_grup['primer_grup']]).ljust(10) + ']'
        linia += '[' + str(nom_grups[preferencies_grup['segon_grup']]).ljust(10) + ']'
        linia += '[' + str(nom_optatives[preferencies_optativa['primera_optativa']]).ljust(11) + ']'
        linia += '[' + str(nom_optatives[preferencies_optativa['segona_optativa']]).ljust(11) + ']'
        linia += '[' + str(nom_optatives[preferencies_optativa['tercera_optativa']]).ljust(11) + ']'
        linia += '[' + str(frances_tercer).ljust(5) + ']'
        print linia
    print ' --  ----------  ----------  -----------  -----------  -----------  -----'

def solucio_aleatoria(alumnes, assignacions_grups_empty, assignacions_optatives_empty):
    assignacions_grups = copy.deepcopy(assignacions_grups_empty)
    assignacions_optatives = copy.deepcopy(assignacions_optatives_empty)
    for k in alumnes.keys():
        assignacions_grups[nom_grups.values()[random.randint(0, 3)]].append(k)
        assignacions_optatives[nom_optatives.values()[random.randint(0, 3)]].append(k)
    return assignacions_grups, assignacions_optatives

def poblacio_aleatoria(alumnes, assignacions_grups_empty, assignacions_optatives_empty, num_poblacions=20):
    poblacio_aleatoria = {}
    for i in range(num_poblacions):
        assignacions_grups, assignacions_optatives = solucio_aleatoria(alumnes, assignacions_grups_empty, assignacions_optatives_empty)
        Q, Q_individuals = funcio_idoneitat(alumnes, assignacions_grups, assignacions_optatives)
        poblacio_aleatoria[i] = {'Q':Q, 'Q_individuals':Q_individuals, 'assignacions_grups':assignacions_grups, 'assignacions_optatives':assignacions_optatives}
    return poblacio_aleatoria

def mostrar_assignacions(alumnes, assignacions_grups, assignacions_optatives):
    print ''
    print '[id][' + 'Grup'.ljust(10) + '][' + 'Optativa'.ljust(11) + ']'
    print ' --  ----------  -----------'
    for id_alumne in alumnes.keys():
        linia = '[' + str(id_alumne).rjust(2) + ']'
        for Grup, membres in assignacions_grups.items():
            if (id_alumne in membres):
                linia += '[' + str(Grup).ljust(10) + ']'
        for Optativa, membres in assignacions_optatives.items():
            if (id_alumne in membres):
                linia += '[' + str(Optativa).ljust(11) + ']'
        print linia
    print ' --  ----------  -----------'

def mostrar_idoneitat(Q, Q_individuals):
    print ''
    print 'Qualitat:', Q
    print ''
    print '[id][ ' + 'Q'.ljust(6) + ']'
    print ' --  -------'
    for id_individu, Q_Q_individu in Q_individuals:
        linia = '[' + str(id_individu).rjust(2) + ']'
        linia += '[' + str(Q_Q_individu).rjust(6) + ']'
        print linia
    print ' --  -------'

def funcio_idoneitat(alumnes, assignacions_grups, assignacions_optatives):
    #inicialitzacio de variables retornades
    Q = 0
    Q_individuals = {}
    # ERROR GREUS: nombre de places superades: grups
    for k, v in nom_grups.items():
        places_assignades = len(assignacions_grups[v])
        if places_assignades > places_grup[k]:
            Q += (places_assignades-places_grup[k]) * violacions_puntuacio['greu']
    # ERROR GREUS: nombre de places superades: optatives
    for k, v in nom_optatives.items():
        places_assignades = len(assignacions_optatives[v])
        if places_assignades > places_optativa[k]:
            Q += (places_assignades-places_optativa[k]) * violacions_puntuacio['greu']
    # ERRORS X ALUMNE
    for k, v in alumnes.items():
        preferencies_grup = v[0]
        preferencies_optativa = v[1]
        frances_tercer = v[2]
        Q_individuals[k] = 0
        # GRUPS
        if not (k in assignacions_grups[nom_grups[preferencies_grup['primer_grup']]]):
            if not (k in assignacions_grups[nom_grups[preferencies_grup['segon_grup']]]):
                # MOLT GREUS: alumne assignat a un grup que no havia triat
                Q += violacions_puntuacio['molt greu']
                Q_individuals[k] += violacions_puntuacio['molt greu']
            else:
                # LLEUS: alumne assinat a un segon grup
                if (k in assignacions_grups[nom_grups[preferencies_grup['segon_grup']]]):
                    Q += violacions_puntuacio['lleu']
                    Q_individuals[k] += violacions_puntuacio['lleu']
        # OPTATIVES
        idoptativa = list(set(nom_optatives.keys()).difference(set(preferencies_optativa.values())))[0]
        if (k in assignacions_optatives[nom_optatives[idoptativa]]):
            # MOLT GREUS: alumne assignat a una optativa que no havia triat
            Q += violacions_puntuacio['molt greu']
            Q_individuals[k] += violacions_puntuacio['molt greu']
        else:
            # LLEU: alumne assinat a una segona optativa
            if (k in assignacions_optatives[nom_optatives[preferencies_optativa['segona_optativa']]]):
                Q += violacions_puntuacio['lleu']
                Q_individuals[k] += violacions_puntuacio['lleu']
            else:
                # GREUS: alumne assinat a una tercera optativa
                if (k in assignacions_optatives[nom_optatives[preferencies_optativa['tercera_optativa']]]):
                    Q += violacions_puntuacio['greu']
                    Q_individuals[k] += violacions_puntuacio['greu']
        # MOLT GREUS: alumne assignat a frances i no ho havia estudiat en tercer d'ESO
        if (k in assignacions_optatives[nom_optatives['4']]) & (frances_tercer == False):
            Q += violacions_puntuacio['molt greu']
            Q_individuals[k] += violacions_puntuacio['molt greu']
    return Q, Q_individuals

def obtenir_individus_progenitors(poblacio_solucions):
    Q_individus_no_ordenat = {}
    for k, v in poblacio_solucions.items():
        Q_individus_no_ordenat[k] = v['Q']
    Q_individus_ordenat = sorted(Q_individus_no_ordenat.items(), key=lambda x: x[1])
    individus_progenitors = []
    for i in range(int(num_poblacions * pecentatge_progenitors)):
        individus_progenitors.append(Q_individus_ordenat[i][0])
    return Q_individus_ordenat, individus_progenitors

def obtenir_encreuaments(individus_progenitors):
    encreuaments = []
    for i in range(num_poblacions):
        encreuaments.append(random.sample(individus_progenitors, 2))
    return encreuaments

def encreua(pares, encreuament, assignacions_grups_empty, assignacions_optatives_empty, alumnes):
    assignacions_grups = copy.deepcopy(assignacions_grups_empty)
    assignacions_optatives = copy.deepcopy(assignacions_optatives_empty)
    for alumne in alumnes:
        if pares[encreuament[0]]['Q_individuals'][alumne] <= pares[encreuament[1]]['Q_individuals'][alumne]:
            for grup in nom_grups.values():
                if alumne in pares[encreuament[0]]['assignacions_grups'][grup]:
                    assignacions_grups[grup].append(alumne)
            for optativa in nom_optatives.values():
                if alumne in pares[encreuament[0]]['assignacions_optatives'][optativa]:
                    assignacions_optatives[optativa].append(alumne)
        else:
            for grup in nom_grups.values():
                if alumne in pares[encreuament[1]]['assignacions_grups'][grup]:
                    assignacions_grups[grup].append(alumne)
            for optativa in nom_optatives.values():
                if alumne in pares[encreuament[1]]['assignacions_optatives'][optativa]:
                    assignacions_optatives[optativa].append(alumne)
    return {'assignacions_grups':assignacions_grups, 'assignacions_optatives':assignacions_optatives}

def obtenir_mutacio(fill, alumnes):
    assignacions_grups = copy.deepcopy(fill['assignacions_grups'])
    assignacions_optatives = copy.deepcopy(fill['assignacions_optatives'])
    mutacio = random.randint(0, len(alumnes)-1)
    if (random.randint(0, 1) < 1):
        # mutar grup
        # treure alumne
        grup_src = ''
        for grup in nom_grups.values():
            if mutacio in assignacions_grups[grup]:
                posi = assignacions_grups[grup].index(mutacio)
                temp = assignacions_grups[grup].pop(posi)
                grup_src = grup
        # mure'l
        grup = nom_grups.values()[random.randint(0, 3)]
        while(grup == grup_src):
            grup = nom_grups.values()[random.randint(0, 3)]
        assignacions_grups[grup].append(mutacio)
    else:
        # mutar optativa
        # treure alumne
        optativa_src = ''
        for optativa in nom_optatives.values():
            if mutacio in assignacions_optatives[optativa]:
                posi = assignacions_optatives[optativa].index(mutacio)
                temp = assignacions_optatives[optativa].pop(posi)
                optativa_src = optativa
        # mure'l
        optativa = nom_optatives.values()[random.randint(0, 3)]
        while(optativa == optativa_src):
            optativa = nom_optatives.values()[random.randint(0, 3)]
        assignacions_optatives[optativa].append(mutacio)
    Q, Q_individuals = funcio_idoneitat(alumnes, assignacions_grups, assignacions_optatives)
    return {'Q':Q, 'Q_individuals':Q_individuals, 'assignacions_grups':assignacions_grups, 'assignacions_optatives':assignacions_optatives}

def evoluciona(alumnes, pares, num_poblacions, num_generacions, pecentatge_progenitors, assignacions_grups_empty, assignacions_optatives_empty):
    cnt_generacio = 0
    while (cnt_generacio < num_generacions):
        # seleccionar els millors
        Q_individus_ordenat, individus_progenitors = obtenir_individus_progenitors(poblacio_solucions)
        # obtenir encreuaments
        encreuaments = obtenir_encreuaments(individus_progenitors)
        # encreuar-los
        fills = {}
        for i in range(num_poblacions):
            fills[i] = encreua(pares, encreuaments[i], assignacions_grups_empty, assignacions_optatives_empty, alumnes)
        # Afegir una mutacio als fills
        mutacio = {}
        for i in range(num_poblacions):
            mutacio[i] = obtenir_mutacio(fills[i], alumnes)
        # print 'ToDo'
        # preparar seguent generacio
        del pares
        pares = copy.deepcopy(mutacio)
        del fills
        del mutacio
        cnt_generacio += 1
    return pares[Q_individus_ordenat[0][0]]['Q'], pares[Q_individus_ordenat[0][0]]['assignacions_grups'], pares[Q_individus_ordenat[0][0]]['assignacions_optatives']

print 'Activitat 4'
print ''

#
# Llegir dades fitxer
#
print ("Llegint dades del fitxer...")
start = time.time()
alumnes = llegir_preferencies_alumnes('alumnes.data')
print 'Temps:', format(time.time()-start, '.2f')
print ''

assignacions_grups_empty = {}
for v in nom_grups.values():
    assignacions_grups_empty[v] = []
assignacions_optatives_empty = {}
for v in nom_optatives.values():
    assignacions_optatives_empty[v] = []

resultats = {}
cnt_resultat = 0
for num_generacions in [10, 100, 1000]:
    for num_poblacions in [20, 60, 100]:
        #
        # Generar poblacio de solucions de forma aleatoria
        #
        print 'Generant poblacio de solucions de forma aleatoria...'
        start = time.time()
        poblacio_solucions = poblacio_aleatoria(alumnes, assignacions_grups_empty, assignacions_optatives_empty, num_poblacions)
        print 'Temps:', format(time.time()-start, '.2f')
        print ''
        #
        # Optimitzacio alg. genetics
        #
        print 'Optimitzacio alg. genetics amb ' + str(num_poblacions) + ' poblacions...'
        start = time.time()
        Q, assignacions_grups, assignacions_optatives = evoluciona(alumnes, poblacio_solucions, num_poblacions, num_generacions, pecentatge_progenitors, assignacions_grups_empty, assignacions_optatives_empty)
        end = time.time()-start
        print 'Temps:', format(end, '.2f')
        print ''
        #
        # Mostrar solucio
        #
        mostrar_assignacions(alumnes, assignacions_grups, assignacions_optatives)
        print 'Q', Q
        resultats[cnt_resultat] = {'poblacions':num_poblacions, 'generacions':num_generacions, 'Q':Q, 'temps':end}
        cnt_resultat += 1
        print ''

print '[Mida poblacio][Num. Generacions][Q     ][Temps     ]'
for resultat in resultats.values():
    linia = '[' + str(resultat['poblacions']).rjust(13) + ']'
    linia += '[' + str(resultat['generacions']).rjust(16) + ']'
    linia += '[' + str(resultat['Q']).rjust(6) + ']'
    linia += '[' + str(format(resultat['temps'], '.2f')).rjust(10) + ']'
    print linia

