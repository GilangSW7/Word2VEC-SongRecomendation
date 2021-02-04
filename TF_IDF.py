import math
import numpy as np
import nltk
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory #steamer Indonesia
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory #stopword indonesia
from nltk.stem import PorterStemmer # Steamer Inggris
from nltk.corpus import stopwords


#Fungsi-fungsi

#fungsi prepro
def prepro(train_documents):

    tokenize = lambda doc: doc.lower().split(" ")
    train_documents_tokenized = [tokenize(d) for d in train_documents]
    print ("Hasil Tokenisasi Dokumen Training: ")
    print (train_documents_tokenized)

    all_tokens_set = set([item for sublist in train_documents_tokenized for item in sublist])
    print ("Term Unik: ")
    all_tokens_set = sorted(all_tokens_set)
    print (all_tokens_set)

    return train_documents_tokenized,all_tokens_set

def Preprocessing(train_documents):
    train_documents = train_documents.translate(str.maketrans('', '', string.punctuation)).lower()
    return nltk.word_tokenize(train_documents)

def uniq_term(train_documents):
    uniq_term = set([item for sublist in train_documents for item in sublist])
    print("Term Unik: ")
    uniq_term = sorted(uniq_term)
    print(uniq_term)
    return uniq_term

def indo_preprocessing(train_documents):

    # #preses steaming bahasa indonesia + Stopword remover
    # factory = StemmerFactory()
    # stemmer = factory.create_stemmer()
    # factory_stop = StopWordRemoverFactory()
    # stopword = factory_stop.create_stop_word_remover()
    #
    # train_documents_stemmed = [stopword.remove(stemmer.stem(d)) for d in train_documents]
    # print ("Hasil Stemming Dokumen Training: ")
    # print (train_documents_stemmed)

    # #proses_tokenisasi( yang pake steam)
    # tokenize = lambda doc: doc.lower().split(" ")
    # train_documents_tokenized = [tokenize(d) for d in train_documents]
    # print ("Hasil Tokenisasi Dokumen Training: ")
    # print (train_documents_tokenized)

    #proses Tokenisai( tanpa steam)
    train_documents_tokenized = []
    # proses Prepro
    for lagu in train_documents:
        # proses tokenisai
        tokens = nltk.word_tokenize(lagu)
        #print(tokens)
        # stopword remover
        # filtered_sentence = [w for w in tokens if not w in stop_words]
        # proses Steaming poter
        steam = []
        # for kata in filtered_sentence :
        #     steam.append(ps.stem(kata))
        train_documents_tokenized.append(tokens)
    print(train_documents_tokenized.__len__())
    #pencarian term uniq
    all_tokens_set = set([item for sublist in train_documents_tokenized for item in sublist])
    # print ("Term Unik: ")
    all_tokens_set = sorted(all_tokens_set)
    # print (all_tokens_set)

    return train_documents_tokenized,all_tokens_set

def eng_preprocessing(train_documents):
    # ps = PorterStemmer()
    # stop_words = set(stopwords.words('english'))
    # #print(stop_words)
    train_documents_tokenized =[]
    #proses Prepro
    for lagu in train_documents:
        #proses tokenisai
        tokens = nltk.word_tokenize(lagu)
        #stopword remover
        #filtered_sentence = [w for w in tokens if not w in stop_words]
        #proses Steaming poter
        steam = []
        # for kata in filtered_sentence :
        #     steam.append(ps.stem(kata))
        train_documents_tokenized.append(tokens)

    #proses uniq term
    all_tokens_set = set([item for sublist in train_documents_tokenized for item in sublist])
    #     print ("Term Unik: ")
    #     all_tokens_set = sorted(all_tokens_set)
    #     print (all_tokens_set)


    return train_documents_tokenized,all_tokens_set


#fungsi LogTF
def log_TF(term,document):
    count = document.count(term)
    if count == 0:
        return 0
    return 1 + math.log10(count)

#Fungsi IDF
def idf(tokenized_documents, all_tokens_set):
    idf_values = {}
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        #print (tkn)
        N =len(tokenized_documents)
        df =sum(contains_token)
        # print (N)
        # print (df)
        idf_values[tkn] = math.log10(N/df)
    return idf_values

#Fungsi TF-IDF
def tfidf(documents, idf):
    tfidf_documents = []
    for document in documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = log_TF(term, document)
            #print(term)
            #print(tf)
            #doc_tfidf[term] = tf * idf[term]
            doc_tfidf.append(tf * idf[term])
            #print (idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

#fungsi normalisasi # bisa dibuat dict coy
def norm (tfidf):
    norm_doc =[]
    for i in range(len(tfidf)):
        pangkat = [x*x for x in tfidf[i]]
        sigmaAkar = math.sqrt(sum(pangkat))
        doc_normalisai =[]
        for j in range(len(tfidf[i])) :
            try:
                doc_normalisai.append(tfidf[i][j]/ sigmaAkar)
            except:
                doc_normalisai.append(tfidf[i][j])
        norm_doc.append(doc_normalisai)
    return norm_doc

#fungsi Cosine
def cosine(norm_doc):
    similarityt = {}
    i = 0
    for doc in norm_doc:
        #print(doc)
        #print(norm_doc[-1])
        cosine = np.dot(doc,norm_doc[-1])
        #print ("hasil cosine")
        #print (cosine)
        similarityt [i] = cosine
        i+=1
    return similarityt

