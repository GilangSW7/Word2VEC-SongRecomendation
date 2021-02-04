#from Sastrawi.Stemmer.StemmerFactory import StemmerFactory #steamer Indonesia
#from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory #stopword indonesia
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# def preprocessing(train_documents):
#
#     #preses steaming bahasa indonesia + Stopword remover
#     factory = StemmerFactory()
#     stemmer = factory.create_stemmer()
#     factory_stop = StopWordRemoverFactory()
#     stopword = factory_stop.create_stop_word_remover()
#
#     train_documents_stemmed = [stopword.remove(stemmer.stem(d)) for d in train_documents]
#     print ("Hasil Stemming Dokumen Training: ")
#     print (train_documents_stemmed)
#
#     #proses_tokenisasi
#     tokenize = lambda doc: doc.lower().split(" ")
#     train_documents_tokenized = [tokenize(d) for d in train_documents_stemmed]
#     print ("Hasil Tokenisasi Dokumen Training: ")
#     print (train_documents_tokenized)
#
#     #pencarian term uniq
#     all_tokens_set = set([item for sublist in train_documents_tokenized for item in sublist])
#     print ("Term Unik: ")
#     all_tokens_set = sorted(all_tokens_set)
#     print (all_tokens_set)
#
#     return train_documents_tokenized,all_tokens_set

def eng_preprocessing(train_documents):
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    #print(stop_words)
    train_documents_tokenized =[]
    #proses Prepro
    for lagu in train_documents:
        #proses tokenisai
        tokens = nltk.word_tokenize(lagu)
        #stopword remover
        filtered_sentence = [w for w in tokens if not w in stop_words]
        #proses Steaming poter
        steam = []
        for kata in filtered_sentence :
            steam.append(ps.stem(kata))
        train_documents_tokenized.append(steam)

    #proses uniq term
    all_tokens_set = set([item for sublist in train_documents_tokenized for item in sublist])
    #     print ("Term Unik: ")
    #     all_tokens_set = sorted(all_tokens_set)
    #     print (all_tokens_set)


    return train_documents_tokenized,all_tokens_set


indo_Corpus = []
eng_Corpus = []


for i in range(1001,1020):
     lagu = open("Lagu/"+str(i)+".txt",'r')
     lirik = str(lagu.read())
     #lirik = "aku adalah kapiten"
     lirik = lirik.translate(str.maketrans('', '', string.punctuation)).lower() #filtering
     indo_Corpus.append(lirik)
     lagu.close()

a,b= eng_preprocessing(indo_Corpus)
print(a)
print(b)