import TF_IDF
import Word2Vec
import string
import csv

indo_Korpus = []
eng_Korpus = []

# #Indo Traning
#mendapatkan korpus dari dokument
for i in range(1,201):
     lagu = open("Lagu/id"+str(i)+".txt",'r')
     lirik = str(lagu.read())
     #lirik = "aku adalah kapiten"
     lirik = lirik.translate(str.maketrans('', '', string.punctuation)).lower() #filtering
     indo_Korpus.append(lirik)
     lagu.close()

#mendapatkan korpus prepro
indo_Korpus_prepro,Indo_Unik = TF_IDF.indo_preprocessing(indo_Korpus)

#w2vec traning
indo_W2V,indo_Repre = Word2Vec.train(indo_Korpus_prepro)
print(indo_Repre)
with open('indo_W2V_NSteam.csv','w',newline='') as my_csv:
     csvWriter = csv.writer(my_csv, delimiter=',')
     csvWriter.writerows(indo_W2V)
with open('indo_Repre_Nsteam.csv','w',newline='') as my_csv:
     csvWriter = csv.writer(my_csv)
     csvWriter.writerow(indo_Repre)

#TF_IDF traning
#idf
idf = TF_IDF.idf(indo_Korpus_prepro,Indo_Unik)
with open('indo_idf_Nsteam.csv', 'w', newline='') as f:
    for key in idf.keys():
        f.write("%s,%s\n" % (key, idf[key]))
#TF-IDF
tfidf = TF_IDF.tfidf(indo_Korpus_prepro,idf)
print(tfidf)
with open('indo_tfidf_Nsteam.csv', 'w',newline='') as my_csv:
    csvWriter = csv.writer(my_csv)
    csvWriter.writerows(tfidf)


# #Eng Traning
# #mendapatkan korpus dari dokument
# for i in range(1,201):
#      lagu = open("Lagu/e"+str(i)+".txt",'r')
#      lirik = str(lagu.read())
#      #lirik = "aku adalah kapiten"
#      lirik = lirik.translate(str.maketrans('','', string.punctuation)).lower() #filtering
#      eng_Korpus.append(lirik)
#      lagu.close()
#
# #mendapatkan korpus prepro
# eng_Korpus_prepro,eng_Unik = TF_IDF.eng_preprocessing(eng_Korpus)
#
# #w2vec traning
# eng_W2V,eng_Repre = Word2Vec.train(eng_Korpus_prepro)
# print(eng_Repre)
# with open('eng_W2V_Nsteam.csv','w',newline='') as my_csv:
#      csvWriter = csv.writer(my_csv, delimiter=',')
#      csvWriter.writerows(eng_W2V)
# with open('eng_Repre_Nsteam.csv','w',newline='') as my_csv:
#      csvWriter = csv.writer(my_csv)
#      csvWriter.writerow(eng_Repre)
#
# #TF_IDF traning
# #idf
# eng_idf = TF_IDF.idf(eng_Korpus_prepro,eng_Unik)
# with open('eng_idf_Nsteam.csv', 'w', newline='') as f:
#     for key in eng_idf.keys():
#         f.write("%s,%s\n" % (key, eng_idf[key]))
# #TF-IDF
# tfidf = TF_IDF.tfidf(eng_Korpus_prepro,eng_idf)
# with open('eng_tfidf_Nsteam.csv', 'w',newline='') as my_csv:
#     csvWriter = csv.writer(my_csv)
#     csvWriter.writerows(tfidf)