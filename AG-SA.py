# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 19:50:13 2020

@author: BRAM
"""

import pandas as pd
import random
import math
import numpy as np

#random.seed(30)
#inisialisasi kromosom
def init_kromosom(indeks):
    #gen[1] = pagi, kromosom[2] = siang, kromosom[3] = malam 
    kromosom = [indeks]
    gen = [[],[],[]] 
#    p0= gen[1][0] - gen[2][0] nilai tetap, gen[2][1] - gen[3][3] ditukar dengan p1
#    p1= gen[1][0] - gen[2][0] nilai tetap, gen[2][1] - gen[3][3] ditukar dengan p0
    for i in range(len(gen)):
        gen[i]= [Karbohidrat[random.randint(0,len(Karbohidrat)-1)],
                              Protein[random.randint(0,len(Protein)-1)],
                              Lemak[random.randint(0,len(Lemak)-1)],
                              Mikronutrien[random.randint(0,len(Mikronutrien)-1)]]
        kromosom.extend(gen[i])
    return kromosom

def Crossover(induk1,induk2,titik_potong):
    c1 = induk1[:titik_potong]+induk2[titik_potong:]
    c2 = induk2[:titik_potong]+induk1[titik_potong:]
    return c1,c2

def Mutasi(induk, titik_tukar):
    m = induk.copy()
    if titik_tukar%4 == 1:
        m[titik_tukar] = Karbohidrat[random.randint(0,len(Karbohidrat)-1)]
    elif titik_tukar%4 == 2:
        m[titik_tukar] = Protein[random.randint(0,len(Protein)-1)]
    elif titik_tukar%4 == 3:
        m[titik_tukar] = Lemak[random.randint(0,len(Lemak)-1)]
    else:
        m[titik_tukar] = Mikronutrien[random.randint(0,len(Mikronutrien)-1)]
    return m

#menghitung total_kalori satu kromosom
def Total_kalori(kromosom):
    jumlah_kalori=0
    for gen in kromosom[1:]:
        jumlah_kalori+=gen[1]
    return jumlah_kalori

#menghitung fitness satu kromosom
def Fitness(kromosom):
    return 100/(1+abs(kebutuhan_kalori-Total_kalori(kromosom)))

#seleksi
def Seleksi(fitness,populasi):
    fitness,populasi = zip(*sorted(zip(fitness, populasi),reverse=True))
    return fitness[:jumlah_populasi],populasi[:jumlah_populasi]

#menampilkan list nama bahan makanan
def Print(pop):
    jumlah_fitness = 0
    for individu in pop:
        print(individu[0],':', end =" ")
        for gen in individu[1:]:
            print(gen[0], end ="; ")
        print(Total_kalori(individu), end ="; ")
        print(Fitness(individu), end ="; ")
        print() 
        jumlah_fitness+=Fitness(individu)
        rerata_fitness =jumlah_fitness/len(pop)
    print('Rata-rata fitness : ',str(rerata_fitness))
    return rerata_fitness
#    print()

def konvergen(rerata, prev_rerata):
    if rerata == prev_rerata:
        return True
    return False


"""
inisialiasasi data dan parameter
"""
# upload daftar makanan
daftar_makanan = pd.read_csv('algen_bahan_makanan.csv')
#print(daftar_makanan.head())

Karbohidrat = []
Protein = []
Lemak = []
Mikronutrien = []


#pemisahan isi tabel sesuai kolom
for i in range(len(daftar_makanan)):
    Kategori = daftar_makanan.Kategori.iloc[i]
    Nama = daftar_makanan.Nama.iloc[i]
    Kalori = daftar_makanan.Kalori.iloc[i]
    #pengelompokkan sesuai kategori
    if (Kategori == 'Karbohidrat'):
        Karbohidrat.append([Nama,Kalori])
    elif (Kategori == 'Protein Hewani') | (Kategori == 'Protein Nabati'):
        Protein.append([Nama,Kalori])
    elif (Kategori == 'Minyak'):
        Lemak.append([Nama,Kalori*0.1])
    elif (Kategori == 'Susu'):
        Lemak.append([Nama,Kalori])
    else:
        Mikronutrien.append([Nama,Kalori])

#inisilisasi parameter
kebutuhan_kalori = 1500
jumlah_populasi = 10
jumlah_generasi = 100
t0 = 0.8
alpha = 0.7
cr = 0.4
mr = 0.4
titik_beku = 0.2
var_Konvergen = 10

#menginisialisasi populasi awal
Populasi = []
for i in range(jumlah_populasi):
    Populasi.append(init_kromosom("i"+str(i+1)))
#print(Populasi)

"""
algoritme genetika
"""
iterasi = 0
rerata = 0
count = 0
#&(t0>titik_beku)
while((iterasi!=jumlah_generasi) &(t0>titik_beku)):
    offspring = []
    #reproduksi
    n_crossover = cr*jumlah_populasi
    n_mutasi = mr*jumlah_populasi
    titik_potong = 4
    titik_tukar = 7
    
    #proses crossover
    for i in range(int(n_crossover/2)):
        induk = random.sample(range(0,len(Populasi)-1), 2)
        c1,c2 = Crossover(Populasi[induk[0]], Populasi[induk[1]], titik_potong)
        c1[0] = 'c'+str(i*2+1)
        c2[0] = 'c'+str(i*2+2)
        offspring.append(c1)
        offspring.append(c2)
    
    #proses mutasi
    for i in range(int(n_mutasi)):
        m = Mutasi(Populasi[random.randint(0,len(Populasi)-1)], titik_tukar)
        m[0] = 'm'+str(i+1)
        offspring.append(m)
    
    #penggabungan populasi awal dan offspring
    Populasi.extend(offspring)
    
    #evaluasi
    #menghitung nilai fitness tiap kromosom
    nilai_fitness=[]
    for kromosom in Populasi:
        nilai_fitness.append(Fitness(kromosom))
            
    #proses seleksi
    fitness, Populasi = Seleksi(nilai_fitness,Populasi)
    
    """
    simulated annealing
    """
    Neighbor, fitness_Neighbor = [],[]
    U = random.random()
    
    #proses Neighbourhood
    for i,individu in enumerate(Populasi):
        n = Mutasi(individu,titik_tukar)
        n[0] = 'n'+str(i+1)
        Neighbor.append(n)
        fitness_Neighbor.append(Fitness(n))
       
    #Print(Populasi)
    #print(U)
    #print(fitness)
    #print()
    #Print(Neighbor)
    #print(fitness_Neighbor)   
    #print()
        
    #proses annealing
    Populasi_baru = []
    for i in range(len(Populasi)):
        selisih_fitness = fitness_Neighbor[i] - fitness[i]
        if selisih_fitness >= 0:
            Populasi_baru.append(Neighbor[i])
        else:
            boltzmann = np.exp(-1*selisih_fitness/t0)
            if U <= boltzmann:
                Populasi_baru.append(Populasi[i])                
            else:
                Populasi_baru.append(Neighbor[i])                
#    individu terpilih  
    for i,individu in enumerate(Populasi_baru):
        individu[0] = 'i'+str(i+1)
#    print(Populasi_baru)
    Populasi = Populasi_baru
#   update suhu    
    t0 *= alpha
    iterasi+=1
    prev_rerata = rerata
    rerata = Print(Populasi)
    print('iterasi ke-'+str(iterasi))
    print()
    if (konvergen(rerata, prev_rerata)):
        count += 1
        if (count >= var_Konvergen) :
            break
    else :
        count = 0


#print(type(Populasi[0]))
#print(type(Neighbor[0]))

#Print(Populasi)
#Print(Neighbor)
#print(Populasi)  
#print(Neighbor)  
#print(len(Populasi))
#print(offspring)