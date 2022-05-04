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
def meme_len (trajet):
	for route in trajet : 
		if trajet[0][1] != route[1]:
			return False
	return True

def transforme(trajet):
	trans = []
	for route in trajet :
		if route[2] == '0':
			trans.append(route[3])
		else :
			trans.append(route[3][::-1])
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

# ouvrir le fichier xml à produire en écriture 
x = open('output.xml','w')

x.write('<?xml version="1.0" encoding="UTF-8"?>\n')
x.write('<!DOCTYPE gedcom SYSTEM "metro.dtd">\n')
x.write('<metro> \n')
station_vu = set () # pour eliminer les doublons on stocke dans station_vu.
for row in data[1:]:
    if row[0] in station_vu : continue # on passe la station si elle existe déjà. 

    station_vu.add(row[0])

    x.write('   <station id="S'+row[0]+'">\n')
    x.write('       <station_name>'+row[1]+'</station_name>\n')
    x.write('       <station_desc>'+row[2]+'</station_desc>\n')
    x.write('       <emplacement>\n')
    x.write('           <station_lat>'+row[3]+'</station_lat>\n')
    x.write('           <station_lon>'+row[4]+'</station_lon>\n')
    x.write('       </emplacement>\n')
    x.write('       <lignes>\n')
    ligne_vu = set()
    for row2 in data[1:]:
        if row2[0] == row[0] in station_vu : 
            if row2[7] in ligne_vu : continue
            ligne_vu.add(row2[7])
            x.write('           <lig idref = "L'+row2[7]+'"/>\n')   
    x.write('       </lignes>\n')
    x.write('   </station>\n')
    x.write('\n')
ligne_vu = set ()
n = 0
for row in data[1:]:
    n = n+1
    if row[7] in ligne_vu : continue

    ligne_vu.add(row[7])

    x.write('   <ligne id ="L'+row[7]+'" short_name ="'+row[9]+'">\n')
    x.write('       <nom_complet>\n')
    x.write('           <first>'+row[10]+'</first>\n')
    x.write('           <last>'+row[11]+'</last>\n')
    x.write('       </nom_complet>\n')
    # Liste des routes 
    i = n
    route_vu = set()
    trajet = []
    while(i<853 and data[i][7] == row[7]):
        i = i+1
        if data[i-1][6] in route_vu : continue

        route_vu.add(data[i-1][6])
        x.write('           <route id="R'+data[i-1][6]+'" direction ="'+data[i-1][8]+'"/>\n')
        count = 0
        m=  0
        arrets = []
        for row3 in data[1:]:
        	m = m+1
        	if row3[6] == data[i-1][6] :
        		count = count+ 1
        		arrets.append(m)
        	
        trajet.append([i,count,data[i-1][8],arrets])
        
    x.write('       <trajet>\n')
    
    #print(trajet)
    trajet_transforme = transforme(trajet)
    #if row[9] == '13' : print(trajet_transforme)
    for i in range(len(trajet_transforme[0])) :
    	station = []
    	for j in range(len(trajet_transforme)) :
    		if data[trajet_transforme[j][i]][0] in station : continue
    		if trajet_transforme[j][i] != 0 : station.append(data[trajet_transforme[j][i]][0])
    	x.write('           <arret>\n')
    	for s in range(len(station)) :
    		x.write('               <station idref = "S'+station[s]+'">\n')
    		for j in range(len(trajet_transforme)):
    			if station[s] == data[trajet_transforme[j][i]][0]:
    				x.write('                   <route idref = "R'+data[trajet_transforme[j][i]][6]+'"/>\n')		
    		x.write('               </station>\n')
    	x.write('           </arret>\n')
    	
    x.write('       </trajet>\n')
    
    
    
    
    x.write('   </ligne>\n')
    x.write('\n')
x.write('</metro>')


		
