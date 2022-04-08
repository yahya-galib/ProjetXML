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

# ouvrir le fichier xml à produire en écriture 
x = open('output.xml','w')

x.write('<?xml version="1.0" encoding="UTF-8"?>\n')
x.write('<Metro> \n')
station_vu = set () # pour eliminer les doublons on stocke dans station_vu.
for row in data[1:]:
    if row[0] in station_vu : continue # on passe la station si elle existe déjà. 

    station_vu.add(row[0])

    x.write('   <station id ="'+row[0]+'">\n')
    x.write('       <station_name>'+row[1]+'</station_name>\n')
    x.write('       <station_desc>'+row[2]+'<station_desc>\n')
    x.write('       <emplacement>\n')
    x.write('           <station_lat>'+row[3]+'<station_lat>\n')
    x.write('           <station_lon>'+row[4]+'<station_lon>\n')
    x.write('       </emplacement>\n')
    x.write('       <lignes>\n')
    ligne_vu = set()
    for row2 in data[1:]:
        if row2[0] == row[0] in station_vu : 
            if row2[7] in ligne_vu : continue
            ligne_vu.add(row2[7])
            x.write('           <lig idref = "'+row2[9]+'"/>\n')   
    x.write('       </lignes>\n')
    x.write('   </station>\n')
    x.write('\n')
ligne_vu = set ()
n = 0
for row in data[1:]:
    n = n+1
    if row[7] in ligne_vu : continue

    ligne_vu.add(row[7])

    x.write('   <ligne id ="'+row[7]+'" short_name ="'+row[9]+'">\n')
    x.write('       <nom_complet>\n')
    x.write('           <first>'+row[10]+'<first>\n')
    x.write('           <last>'+row[11]+'<last>\n')
    x.write('       </nom_complet>\n')
    i = n
    route_vu = set()
    while(i<853 and data[i][7] == row[7]):
        i = i+1
        if data[i-1][6] in route_vu : continue

        route_vu.add(data[i-1][6])
        x.write('       <route id = "'+data[i-1][6]+'">\n')
        x.write('           <direction>'+data[i-1][8]+'</direction>\n')
        for row3 in data[1:]:
            if row3[6] == data[i-1][6] :
                x.write('              <arret idref = "'+row3[0]+'" index = "'+row3[5]+'"/>\n')
        x.write('       </route>\n')
    x.write('   </ligne>\n')
    x.write('\n')
x.write('</Metro>')
