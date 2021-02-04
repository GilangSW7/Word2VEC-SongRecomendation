import numpy as np


#parameter
ETA = 0.025 # eror rate #learning rate
#win_size = 1
NEURON = 7 #Dimension size(windows size = neuron/2)
uniq =0
w1=w2=repre=[]
epoch = 110 #100 #iterasi


#Corpus =[['i','want','something','just','like','this','like','like'],['i','want']]
Corpus = [[ "i","want","something","just","like","this"]]
#Corpus = [[ "aku","adalah","kapiten"]]

def train(corpus):
    print("jalan boy")
    global w1,w2,repre,uniq
    #uniq words
    repre = list (set([item for sublist in corpus for item in sublist]))
    repre.sort()
    uniq =len(repre)

    #random matrix w1 as context matrix and w2 as embedding matrix
    w1 = np.random.uniform(-1.0, 1.0, (uniq, NEURON))
    #w1 = np.array([[0.5,0.1,-0.2],[0.4,0.5,0.6],[-0.3,0.2,0.3],[-0.7,0.7,0.4],[0.4,0.2,0.5],[0.1,0.1,0.6]])
    #w2 = np.array([[-0.2,0.2,-0.1,0.7,-0.7,0.4],[0.6,0.5,-0.2,0.4,0.2,-0.3],[0.1,-0.7,0.4,0.6,-0.5,0.2]])
    w2 = np.random.uniform(-1.0, 1.0, (NEURON, uniq))

    encode = onehot_Encode(corpus)
    print(encode.__len__())
    for i in range (epoch):
        j = 0
        for w, w_neig in encode:
            print("proses ke "+str(i))
            j = j+1
            print(j)
            # print(w1)
            # FORWARD PASS
            y_pred, h, u = forward_pass(w)
            # print(u)

            # CALCULATE ERROR
            EI = np.sum([np.subtract(y_pred, word) for word in w_neig], axis=0)

            # BACKPROPAGATION
            backprop(EI, h, w)
    #print(len(w1))
    # print("EPOCH :" + str(i))
    return w1,repre



#onehotEncode
def onehot_Encode(corpus):
    #tetangga
    plus,neg = count_neg(NEURON)
    # one hot encode
    Encode = []
    for lyric in corpus:
        for i in range (len(lyric)) :
            w = datGen(lyric[i])
            w_neig = []
            temp = neg
            for j in range(plus):
                j+=1
               # print(lyric[i])
                if i+j < len(lyric):
                    #print(lyric[i+j])
                    w_neig.append(datGen(lyric[i+j]))
                if i-j >=0 and temp !=0:
                    #print(lyric[i-j])
                    w_neig.append(datGen(lyric[i-j]))
                    temp-=1
            Encode.append([w, w_neig])
            #print(Encode)
    return Encode

#data generation
def datGen(kata):
    gen = [0 for i in range(len(repre))]
    gen[repre.index(kata)] = 1
    return gen

#perhitungan tetangga
def count_neg(neuron):
    neuron = neuron -1
    return int(np.ceil(neuron/2)), int(neuron/2)

#forward pass
def forward_pass(word_gen):
    h = np.dot(w1.T, word_gen)
    u = np.dot(w2.T, h)
    e_x = np.exp(u - np.max(u))
    y_c = e_x / e_x.sum(axis=0)
    return y_c, h, u

#backprop
def backprop(e, h, x):
    global w1,w2
    dl_dw2 = np.outer(h, e)
    dl_dw1 = np.outer(x, np.dot(w2, e.T))
    # print('dldw1')
    # print(len(dl_dw1))
    # print(len(dl_dw1[0]))
    # print('w1')
    # print(len(w1))
    # print(len(w1[0]))
# update w1 and w2
    w1 = w1 - (ETA * dl_dw1)
    w2 = w2 - (ETA * dl_dw2)

def kata_dekat(kata,top_n,w1,repre):
    try:
        index_kata = repre.index(kata) # bisa dihilangin klo dari awal pke dict
        v_w1 = w1[index_kata]
        kedekatan_kata = []
        for i in range(len(w1)):
            v_w2 = w1[i] #sebenrnya gak penting
            theta_num = np.dot(v_w1, v_w2)
            theta_den = np.linalg.norm(v_w1) * np.linalg.norm(v_w2)
            theta = theta_num / theta_den

            kedekatan_kata.append([repre[i], theta])
        kedekatan_kata.sort(key=lambda x: x[1] ,reverse=True)
        kata =[x[0] for x in kedekatan_kata[1:top_n]]
    except:
        kata =[]
    return kata #kedekatan_kata [1:top_n]

#train(Corpus)
#print(repre)
#print(kata_dekat("something",3))
