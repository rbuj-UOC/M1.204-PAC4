import math
import time

import copy
import random

nom_grups = {'1':'cientific', '2':'tecnologic', '3':'humanistic', '4':'artistic'}
nom_optatives = {'1':'informatica', '2':'llati', '3':'teatre', '4':'frances'}
violacions_puntuacio = {'lleu':10 ** 0, 'greu':10 ** 1, 'molt greu':10 ** 3}
places_grup = {'1':20, '2':20, '3':30, '4':30}
places_optativa = {'1':25, '2':25, '3':25, '4':25}

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

def solucio_aleatoria(alumnes):
    assignacions_grups = {}
    for v in nom_grups.values():
        assignacions_grups[v] = []
    assignacions_optatives = {}
    for v in nom_optatives.values():
        assignacions_optatives[v] = []
    for k in alumnes.keys():
        assignacions_grups[nom_grups.values()[random.randint(0, 3)]].append(k)
        assignacions_optatives[nom_optatives.values()[random.randint(0, 3)]].append(k)
    return assignacions_grups, assignacions_optatives

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

def funcio_error(alumnes, assignacions_grups, assignacions_optatives):
    #inicialitzacio de variables retornades
    error = 0
    # ERROR GREUS: nombre de places superades: grups
    for k, v in nom_grups.items():
        places_assignades = len(assignacions_grups[v])
        if places_assignades > places_grup[k]:
            error += (places_assignades-places_grup[k]) * violacions_puntuacio['greu']
    # ERROR GREUS: nombre de places superades: optatives
    for k, v in nom_optatives.items():
        places_assignades = len(assignacions_optatives[v])
        if places_assignades > places_optativa[k]:
            error += (places_assignades-places_optativa[k]) * violacions_puntuacio['greu']
    # ERRORS X ALUMNE
    for k, v in alumnes.items():
        preferencies_grup = v[0]
        preferencies_optativa = v[1]
        frances_tercer = v[2]
        # GRUPS
        if not (k in assignacions_grups[nom_grups[preferencies_grup['primer_grup']]]):
            if not (k in assignacions_grups[nom_grups[preferencies_grup['segon_grup']]]):
                # MOLT GREUS: alumne assignat a un grup que no havia triat
                error += violacions_puntuacio['molt greu']
            else:
                # LLEUS: alumne assinat a un segon grup
                if (k in assignacions_grups[nom_grups[preferencies_grup['segon_grup']]]):
                    error += violacions_puntuacio['lleu']
        # OPTATIVES
        idoptativa = list(set(nom_optatives.keys()).difference(set(preferencies_optativa.values())))[0]
        if (k in assignacions_optatives[nom_optatives[idoptativa]]):
            # MOLT GREUS: alumne assignat a una optativa que no havia triat
            error += violacions_puntuacio['molt greu']
        else:
            # LLEU: alumne assinat a una segona optativa
            if (k in assignacions_optatives[nom_optatives[preferencies_optativa['segona_optativa']]]):
                error += violacions_puntuacio['lleu']
            else:
                # GREUS: alumne assinat a una tercera optativa
                if (k in assignacions_optatives[nom_optatives[preferencies_optativa['tercera_optativa']]]):
                    error += violacions_puntuacio['greu']
        # MOLT GREUS: alumne assignat a frances i no ho havia estudiat en tercer d'ESO
        if (k in assignacions_optatives[nom_optatives['4']]) & (frances_tercer == False):
            error += violacions_puntuacio['molt greu']
    return error

def genera_vei(nova_assignacions_grups, nova_assignacions_optatives, estats_previs_grups, estats_previs_optatives):
    if (random.randint(0, 1) < 1):
        #
        # modificar grup
        #
        # triar a l'atzar un alumne
        alumnes_disponibles = alumnes.keys()
        alumne = alumnes_disponibles[random.randint(0, len(alumnes_disponibles)-1)]
        alumnes_disponibles = list(set(alumnes.keys()).difference(set([alumne])))
        # obtenir els grups no assignats
        grups_disponibles = []
        for v in nom_grups.values():
            if not alumne in estats_previs_grups[v]:
                grups_disponibles.append(v)
        while(len(grups_disponibles) < 1):
            alumne = alumnes_disponibles[random.randint(0, len(alumnes_disponibles)-1)]
            alumnes_disponibles = list(set(alumnes.keys()).difference(set([alumne])))
            # obtenir els grups no assignats
            grups_disponibles = []
            for v in nom_grups.values():
                if not alumne in estats_previs_grups[v]:
                    grups_disponibles.append(v)
        grup = grups_disponibles[random.randint(0, len(grups_disponibles)-1)]
        # obtenir els grup actualment assignat i treure'l
        for v in nom_grups.values():
            if alumne in nova_assignacions_grups[v]:
                posi = nova_assignacions_grups[v].index(alumne)
                tbd = nova_assignacions_grups[v].pop(posi)
                if tbd != alumne:
                    print 'Error'
        if alumne in nova_assignacions_grups[grup]:
            print 'Error', grup
        nova_assignacions_grups[grup].append(alumne)
    else:
        #
        # modificar optativa
        #
        # trier a l'atzar una optativa amb almenys dos elements
        # triar a l'atzar un alumne
        alumnes_disponibles = alumnes.keys()
        alumne = alumnes_disponibles[random.randint(0, len(alumnes_disponibles)-1)]
        alumnes_disponibles = list(set(alumnes.keys()).difference(set([alumne])))
        # obtenir els grups no assignats
        optatives_disponibles = []
        for v in nom_optatives.values():
            if not alumne in estats_previs_optatives[v]:
                optatives_disponibles.append(v)
        while(len(optatives_disponibles) < 1):
            alumne = alumnes_disponibles[random.randint(0, len(alumnes_disponibles)-1)]
            alumnes_disponibles = list(set(alumnes.keys()).difference(set([alumne])))
            # obtenir els grups no assignats
            optatives_disponibles = []
            for v in nom_grups.values():
                if not alumne in estats_previs_optatives[v]:
                    optatives_disponibles.append(v)
        optativa = optatives_disponibles[random.randint(0, len(optatives_disponibles)-1)]
        # obtenir els grup actualment assignat i treure'l
        for v in nom_optatives.values():
            if alumne in nova_assignacions_optatives[v]:
                posi = nova_assignacions_optatives[v].index(alumne)
                tbd = nova_assignacions_optatives[v].pop(posi)
                if tbd != alumne:
                    print 'Error'
        if alumne in nova_assignacions_optatives[optativa]:
            print 'Error', optativa
        nova_assignacions_optatives[optativa].append(alumne)
    return nova_assignacions_grups, nova_assignacions_optatives, estats_previs_grups, estats_previs_optatives

def accepta(energia, novaEnergia, iteracions, factor):
    if novaEnergia < energia:
        return True
    else:
        valor = math.exp((energia-novaEnergia) /
                         (iteracions * factor))
        return random.random() < valor

def funcio_error_mig(alumnes):
    numAlumnes = float(len(alumnes))
    error = violacions_puntuacio['lleu'] * numAlumnes * 1
    error += violacions_puntuacio['greu'] * numAlumnes * 0.75
    error += violacions_puntuacio['molt greu'] * numAlumnes * 0.15
    return int (error)

def recoccioSimulada(assignacions_grups, assignacions_optatives, tolerancia, iteracions):
    factor = tolerancia / float(iteracions)
    estats_previs_grups = copy.deepcopy(assignacions_grups)
    estats_previs_optatives = copy.deepcopy(assignacions_optatives)
    iteracio = 0
    # el millor resultat obtingut es el que es retorna
    nova_assignacions_grups = copy.deepcopy(assignacions_grups)
    nova_assignacions_optatives = copy.deepcopy(assignacions_optatives)
    millor_assignacions_grups = copy.deepcopy(assignacions_grups)
    millor_assignacions_optatives = copy.deepcopy(assignacions_optatives)
    millor_error = funcio_error(alumnes, assignacions_grups, assignacions_optatives)
    error = funcio_error_mig(alumnes)
    while iteracio < iteracions:
        nova_assignacions_grups, nova_assignacions_optatives, estats_previs_grups, estats_previs_optatives = genera_vei(nova_assignacions_grups, nova_assignacions_optatives, estats_previs_grups, estats_previs_optatives)
        nou_error = funcio_error(alumnes, nova_assignacions_grups, nova_assignacions_optatives)
        if accepta(error, nou_error, iteracions, factor):
            error = nou_error
            del assignacions_grups
            del assignacions_optatives
            assignacions_grups = copy.deepcopy(nova_assignacions_grups)
            assignacions_optatives = copy.deepcopy(nova_assignacions_optatives)
            if (nou_error < millor_error):
                del millor_assignacions_grups
                del millor_assignacions_optatives
                millor_assignacions_grups = copy.deepcopy(nova_assignacions_grups)
                millor_assignacions_optatives = copy.deepcopy(nova_assignacions_optatives)
                millor_error = nou_error
        del nova_assignacions_grups
        del nova_assignacions_optatives
        nova_assignacions_grups = copy.deepcopy(assignacions_grups)
        nova_assignacions_optatives = copy.deepcopy(assignacions_optatives)
        iteracio += 1
    return millor_error, millor_assignacions_grups, millor_assignacions_optatives

print 'Activitat 3'
print ''

#
# Llegir dades fitxer
#
print ("Llegint dades del fitxer...")
alumnes = llegir_preferencies_alumnes('alumnes.data')
print ''

#
# Generar solucio aleatoria
#
print 'Generant una solucio aleatoria...'
assignacions_grups, assignacions_optatives = solucio_aleatoria(alumnes)
#
# Funcio error
#
error = funcio_error(alumnes, assignacions_grups, assignacions_optatives)
mostrar_assignacions(alumnes, assignacions_grups, assignacions_optatives)
print ''
print 'Error:', error
print ''

#
# Recoccio simulada
#
tolerancia = 10000.0
iteracions = 100000
print 'Recoccio simulada...'
start = time.time()
error, assignacions_grups, assignacions_optatives = recoccioSimulada(assignacions_grups, assignacions_optatives, tolerancia, iteracions)
print 'Temps reccoccio simulada:', format(time.time()-start, '.2f'), 'segons'
mostrar_assignacions(alumnes, assignacions_grups, assignacions_optatives)
print ''
print 'Error:', error
