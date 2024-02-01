import random
nom_grups = {'1':'cientific', '2':'tecnologic', '3':'humanistic', '4':'artistic'}
nom_optatives = {'1':'informatica', '2':'llati', '3':'teatre', '4':'frances'}

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

print 'Activitat 1'
print ''

#
# Llegir dades fitxer
#
print ("Llegint dades del fitxer...")
alumnes = llegir_preferencies_alumnes('alumnes.data')
print ''

#
# Mostrar llistat alumnes
#
print 'Llistat alumnes:'
mostar_preferencies_alumnes(alumnes)
print ''

#
# Generar solucio aleatoria
#
print 'Generant una solucio aleatoria...'
assignacions_grups, assignacions_optatives = solucio_aleatoria(alumnes)
print ''

#
# Mostrar solucio aleatoria
#
print 'Assignacio:'
mostrar_assignacions(alumnes, assignacions_grups, assignacions_optatives)