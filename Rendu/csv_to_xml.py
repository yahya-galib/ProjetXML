import csv

# ouvrir le fichier csv
f = open('base_ratp.csv')

# lire le fichier avec le delimiter ';'
csv_f = csv.reader(f,delimiter=';')

data = []
# parcourir le fichier et stocker dans un tableau
for row in csv_f:
    data.append(row)

# ferme le fichier 
f.close()

# Liste de definition 
def transforme(trajet):
	trans = []
	for route in trajet :
		if route[0] == '0':
			trans.append(route[1])
		else :
			trans.append(route[1][::-1])
	for i in range(0,len(trans),2):
		if len(trans[i]) != len(trans[i+1]) :
			last_same = -1
			r = 0
			diff = 0
			if len(trans[i]) < len(trans[i+1]) :
				r = len(trans[i])
				diff = len(trans[i+1]) - len(trans[i])
			else :
				r = len(trans[i+1])
				diff = len(trans[i]) - len(trans[i+1])
			for j in range(r) :
				if data[trans[i][j]][0] == data[trans[i+1][j]][0] :
					last_same = j
				else :	
					for m in range(diff):
						if last_same == -1 :
							if len(trans[i]) < len(trans[i+1]) :
								trans[i].insert(0,0)
							else : 
								trans[i+1].insert(0,0)
						else : 
							if len(trans[i]) < len(trans[i+1]) :
								trans[i].append(0)
							else : 
								trans[i+1].append(0)
					break	
	return trans

def transformea(trajet):
	trans = []
	# Met les routes retours dans le même sens
	for route in trajet :
		if route[0] == '0':
			trans.append(route[1])
		else :
			trans.append(route[1][::-1])
			
	# Remplie les trous par 0
	for i in range(0,len(trans),2):
	    while len(trans[i]) != len(trans[i+1]) :
	        last_same = -1
	        while len(trans[i]) < len(trans[i+1]) :
	            last = -1
	            for j in range(len(trans[i])) :
	                if data[trans[i+1][j]][0] == data[trans[i][j]][0] :
	                    last = j
	                else :
	                    trans[i].insert(last + 1, 0)
	                    break
	            if last == len(trans[i]) - 1 :
	                for m in range(len(trans[i+1]) - len(trans[i])) :
	                    trans[i].append(0)
	        else :
	            trans[i+1].append(0)

	return trans

test = [['0',[3,4,5]],['0',[1,2,3,4,5,6]]]
print(test)
print(transforme(test))
test2 = [['0',[1,2,3]],['0',[1,2,3,4,5,6]]]
print(test2)
print(transforme(test2))


# ouvrir le fichier xml à produire en écriture 
x = open('output.xml','w')

# Début écriture du fichier xml
x.write('<?xml version="1.0" encoding="UTF-8"?>\n')
x.write('<!DOCTYPE gedcom SYSTEM "metro.dtd">\n')
x.write('<metro> \n')

# On commence le fichier XML par la liste de toutes les stations
# Pour eliminer les doublons on stocke dans station_vu.
station_vu = set () 
for row in data[1:]:
    # On passe la station si elle existe déjà. 
    if row[0] in station_vu : continue 
    station_vu.add(row[0])
    
    # Description d'une Station avec son id, nom, address et coordonnées
    x.write('   <station id="S'+row[0]+'">\n')
    x.write('       <station_name>'+row[1]+'</station_name>\n')
    x.write('       <station_desc>'+row[2]+'</station_desc>\n')
    x.write('       <emplacement>\n')
    x.write('           <station_lat>'+row[3]+'</station_lat>\n')
    x.write('           <station_lon>'+row[4]+'</station_lon>\n')
    x.write('       </emplacement>\n')
    x.write('       <lignes>\n')
    
    # La liste des lignes qui passe par cette station (Corespondance)
    ligne_vu = set()   
    for row2 in data[1:]:
        if row2[0] == row[0] in station_vu : 
            if row2[7] in ligne_vu : continue
            ligne_vu.add(row2[7])
            x.write('           <lig idref = "L'+row2[7]+'"/>\n')   
            
    x.write('       </lignes>\n')
    x.write('   </station>\n')
    x.write('\n')

# On rajoute la liste de toutes les lignes
ligne_vu = set () 
n = 0
for row in data[1:]:
    # On passe la ligne si elle existe déja
    n = n+1
    if row[7] in ligne_vu : continue
    ligne_vu.add(row[7])
    
    # Description de la ligne avec son nom complet et numero
    x.write('   <ligne id ="L'+row[7]+'" short_name ="'+row[9]+'">\n')
    x.write('       <nom_complet>\n')
    x.write('           <first>'+row[10]+'</first>\n')
    x.write('           <last>'+row[11]+'</last>\n')
    x.write('       </nom_complet>\n')
    
    # Liste des routes que possèdent une ligne
    i = n
    route_vu = set()
    trajet = [] 
    while(i<853 and data[i][7] == row[7]):
        i = i+1
        if data[i-1][6] in route_vu : continue

        route_vu.add(data[i-1][6])
        x.write('           <route id="R'+data[i-1][6]+'" direction ="'+data[i-1][8]+'"/>\n')
        count = 0
        m =  0
        arrets = []
        for row3 in data[1:]:
        	m = m+1
        	if row3[6] == data[i-1][6] :
        		count = count+ 1
        		arrets.append(m)        	
        trajet.append([data[i-1][8],arrets])        
    
    # On rajoute le trajet principale d'une ligne
    x.write('       <trajet>\n')
    print(row[9])
    print(trajet)
    print()
    trajet_transforme = transforme(trajet)
    print(trajet)
    print()
    print(trajet_transforme)
    for i in range(len(trajet_transforme[0])) :
    	station = []
    	# Liste des stations pour chaque arret
    	for j in range(len(trajet_transforme)) :
    		if data[trajet_transforme[j][i]][0] in station : continue
    		if trajet_transforme[j][i] != 0 : station.append(data[trajet_transforme[j][i]][0])
    	# On rajoute un arret
    	x.write('           <arret>\n')
    	
    	# On rajoute la list des stations de l'arret
    	for s in range(len(station)) :
    		x.write('               <station idref = "S'+station[s]+'">\n')
    		
    		# On rajoute les references des routes auxquels appartient l'arret
    		for j in range(len(trajet_transforme)):
    			if station[s] == data[trajet_transforme[j][i]][0]:
    				x.write('                   <route idref = "R'+data[trajet_transforme[j][i]][6]+'"/>\n')	
    					
    		x.write('               </station>\n')
    	x.write('           </arret>\n')  	
    x.write('       </trajet>\n')    
    x.write('   </ligne>\n')
    x.write('\n')
x.write('</metro>')


		
