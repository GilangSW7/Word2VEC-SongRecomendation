import string
import csv
import Word2Vec
import TF_IDF
import Terjemahan

indo_idf = {}
eng_idf = {}
indo_tfidf = []
eng_tfidf = []
indo_w2v = []
eng_w2v = []
indo_repre = []
eng_repre = []
hasil = {}
dafatar_lagu = {}

#parameter
kata_Dekat = 3 # queri expansian
kata_TFIDF = 10  # tf idf tertinggi

#proses pengambilan data

#pengambilan data idf indonesia
with open('indo_idf_Nsteam.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in data:
        indo_idf[row[0]] = float(row[1])

#proses pengambilan data indo tf-idf
with open('indo_tfidf_Nsteam.csv', newline='') as csvfile:
    # data = csv.reader(csvfile, delimiter=',', quotechar='|')
    # for row in data:
    #     #print(row)
    #     indo_tfidf.append(row)
    #indo_tfidf=list(data)
    indo_tfidf = [list(map(float, row)) for row in csv.reader(csvfile, delimiter=',', quotechar='|')]

#proses pengambilan indo w2v
with open('indo_W2V_Nsteam.csv', newline='') as csvfile:
    #data = csv.reader(csvfile, delimiter=',', quotechar='|')
    indo_w2v=[list(map(float, row)) for row in csv.reader(csvfile, delimiter=',', quotechar='|')]

#pengambilan data idf inggris
with open('eng_idf_Nsteam.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in data:
        eng_idf[row[0]] = float(row[1])

#proses pengambilan data eng tf-idf
with open('eng_tfidf_Nsteam.csv', newline='') as csvfile:
    eng_tfidf = [list(map(float, row)) for row in csv.reader(csvfile, delimiter=',', quotechar='|')]

#proses pengambilan eng w2v
with open('eng_W2V_Nsteam.csv', newline='') as csvfile:
    #data = csv.reader(csvfile, delimiter=',', quotechar='|')
    eng_w2v=[list(map(float, row)) for row in csv.reader(csvfile, delimiter=',', quotechar='|')]

#proses pengambilan Reperesentasi kata w2v indo
with open('indo_Repre_Nsteam.csv', newline='') as csvfile:
     data = csv.reader(csvfile, delimiter=',', quotechar='|')
     indo_repre=list(data)

#proses pengambilan Reperesentasi kata w2v inggris
with open('eng_Repre_Nsteam.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=',', quotechar='|')
    eng_repre = list(data)

#proses pengambilan data lagu
with open('lagu.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in data:
        #print(row)
        dafatar_lagu[row[0]] = row[1]

#print(indo_repre[0])

#pembuatan TF-Idf Baru
def new_TFIDF(tfidf,idf,tfidfdata,term,w1,repre) :
    dict = {}
    i = 0
    for key in idf.keys():
        dict[key] = tfidf[0][i]
        i+=1
    dict = sorted(dict.items(), key=lambda x: x[1],reverse=True)
    #print(dict)
    kata = []
    for i in range(len(dict[:kata_TFIDF])):
        kata.append([dict[i][0],term[0].count(dict[i][0])])
        #print(dict[i])
    print("kata TF-IDF")
    print(kata)

    for word in kata:
        add_word = Word2Vec.kata_dekat(word[0],kata_Dekat,w1,repre)
        print("kata yang ditambahkan")
        print(add_word)
        for j in range(word[1]):
            term[0] += add_word
        #print(term)
    return tfidfdata + TF_IDF.tfidf(term,idf) #proses nambahain tf idf lama sama queri

#fungsi Cross language
def cross_TFIDF(tfidf,idf,tfidfcross,idfcross,term,w1,repre,a) :
    dict = {}
    croosTerm= []
    i = 0
    for key in idf.keys():
        dict[key] = tfidf[0][i]
        i+=1
    dict = sorted(dict.items(), key=lambda x: x[1],reverse=True)
    #print(dict)
    kata = []
    for i in range(len(dict)):
        kata.append([dict[i][0],term[0].count(dict[i][0])])

    #proses penerjemahan
    terjemahan = []
    for word in kata[:kata_TFIDF]:
        for k in range(word[1]):
            terjemahan.append(Terjemahan.translator.translate(word[0],dest=a).text)
    croosTerm.append(terjemahan)

    for word in kata[:kata_TFIDF]:
        #print(Terjemahan.translator.translate(word[0],dest=a).text)
        add_word = Word2Vec.kata_dekat(Terjemahan.translator.translate(word[0],dest=a).text,kata_Dekat,w1,repre)
        #print(add_word)
        for j in range(word[1]):
            croosTerm[0] += add_word
        #print(term)
    ayam = TF_IDF.tfidf(croosTerm,idfcross)
    return tfidfcross + TF_IDF.tfidf(croosTerm,idfcross) #proses nambahain tf idf lama sama queri

#print(eng_idf.keys())
input = input("Masukan Kode lagu :")
#print(input)
print("Lagu Inputan : " +dafatar_lagu[input])

try:
    kueri = []
    lagu = open("Lagu/"+input+".txt",'r')
    lirik = str(lagu.read())
    lirik = lirik.translate(str.maketrans('', '', string.punctuation)).lower() #filtering
    kueri.append(lirik)
    lagu.close()
except:
    print("Kode lagu Tidak ada di Dataset")


if 'e' in input:
    print('Lagu Berbahasa Inggris')
    term , unik = TF_IDF.eng_preprocessing(kueri)
    tfidf = TF_IDF.tfidf(term,eng_idf)

    newtfidf = new_TFIDF(tfidf,eng_idf,eng_tfidf,term,eng_w2v,eng_repre[0])
    #print(newtfidf)
    simiarity = TF_IDF.cosine(TF_IDF.norm(newtfidf))

    #proses crooss
    crosstfidf = cross_TFIDF(tfidf,eng_idf,indo_tfidf,indo_idf,term,indo_w2v,indo_repre,'id')
    cSimilarity = TF_IDF.cosine(TF_IDF.norm(crosstfidf))
    #print('croos TF idf')
    #print(crosstfidf)

    for i in range(len(simiarity)-1):
        hasil['en'+str(i+1)]=simiarity[i]
        hasil['id' + str(i + 1)] = cSimilarity[i]

elif 'i' in input:
    print('Lagu Berbahasa Indonesia')
    term, unik = TF_IDF.indo_preprocessing(kueri)
    tfidf = TF_IDF.tfidf(term, indo_idf)

    newtfidf = new_TFIDF(tfidf, indo_idf, indo_tfidf, term, indo_w2v, indo_repre[0])
    #print(newtfidf)
    simiarity = TF_IDF.cosine(TF_IDF.norm(newtfidf))

    # proses crooss
    #crosstfidf = cross_TFIDF(tfidf, indo_idf, eng_tfidf, eng_idf, term, eng_w2v, eng_repre, 'en')
    #cSimilarity = TF_IDF.cosine(TF_IDF.norm(crosstfidf))

    for i in range(len(simiarity) - 1):
        hasil['id' + str(i + 1)] = simiarity[i]
        #hasil['en' + str(i + 1)] = cSimilarity[i]

#print(hasil)
hasil = sorted(hasil.items(), key=lambda x: x[1],reverse=True)
print()
print('<<<<HASIL REKOMENDASI>>>>')
# cetak isi file dengan perulangan
for judul in range(1,11):
    print(dafatar_lagu[hasil[judul][0]] + str(hasil[judul]))



