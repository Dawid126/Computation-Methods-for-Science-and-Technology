from nltk.corpus import stopwords
import numpy as np
from nltk.stem import PorterStemmer
from scipy import sparse
from scipy.sparse import csr_matrix, hstack, lil_matrix, coo_matrix
import math
import scipy
import ast
from scipy.sparse.linalg import svds, eigs
import gc

#nltk.download() #- modules/punkt
#nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

n = 2070
k = 50
l = 5


def create_dictionary():
    dictionary = {}
    counter = 0
    links = open('links.txt', 'r')
    for i in range(n):
        file_name = "files/" + links.readline().split("/")[3].split('\n')[0] + ".txt"
        file = open(file_name, 'r', encoding='utf-8')
        for line in file:
            for word in line.split():
                stemmed_word = ps.stem(word)
                if (stemmed_word not in stop_words and stemmed_word not in dictionary):
                    dictionary[stemmed_word] = counter
                    counter = counter + 1

    links.close()
    dictionary_file = open("dictionary.txt", 'w+', encoding='utf-8')
    dictionary_file.write(str(dictionary))
    dictionary_file.close()


def create_links_dictionary():
    dictionary = {}
    counter = 0
    links = open('links.txt', 'r')
    for i in range(n):
        dictionary[counter] = links.readline()
        counter = counter + 1

    links.close()
    links_dictionary_file = open("links_dictionary.txt", 'w+', encoding='utf-8')
    links_dictionary_file.write(str(dictionary))
    links_dictionary.close()


def create_term_by_document_matrix(dictionary, m):
    tbdm = coo_matrix((m, 0))
    links = open('links.txt', 'r')
    for i in range(n):
        file_name = "files/" + links.readline().split("/")[3].split("\n")[0] + ".txt"
        vector = create_bag_of_words(file_name, dictionary, m)
        tbdm = hstack([tbdm, vector])

    tbdm = lil_matrix(tbdm)
    for i in range(m):
        nw = 0
        for j in range(n):
            if(tbdm[i, j] != 0):
                nw = nw + 1

        if(nw == 0):
            print("Some of the input words are not present in the dictionary")
            exit(-1)

        idf = math.log10(n / nw)
        for j in range(n):
            tbdm[i, j] = tbdm [i, j] * idf


    for j in range(n):
        length_to_power = 0
        for i in range(m):
            length_to_power = length_to_power + tbdm[i, j] ** 2

        length_to_power = math.sqrt(length_to_power)
        for i in range(m):
            tbdm[i, j] = tbdm[i, j] / length_to_power


    tbdm = csr_matrix(tbdm)
    scipy.sparse.save_npz('tbdm_sparse.npz', tbdm)


def create_bag_of_words(path, dictionary, m):
    file = open(path, 'r', encoding='utf-8')
    vector = lil_matrix((m, 1))
    for line in file:
        for word in line.split():
            stemmed_word = ps.stem(word)

            if (stemmed_word not in stop_words):
                tmp = vector[dictionary[stemmed_word], 0]
                tmp = tmp + 1
                vector[dictionary[stemmed_word], 0] = tmp

    return coo_matrix(vector)


def calculate_prob_matrix(tbdm, dictionary, m, q):
    q_transposed = np.zeros(m)
    length_to_power = 0

    for word in q.split():
        stemmed_word = ps.stem(word)

        if(stemmed_word not in stop_words):
            q_transposed[dictionary[stemmed_word]] = q_transposed[dictionary[stemmed_word]] + 1

    for i in range(m):
        length_to_power = length_to_power + q_transposed[i] ** 2

    for i in range(m):
        q_transposed[i] = q_transposed[i] / length_to_power

    q_transposed = csr_matrix(q_transposed)
    tbdm = csr_matrix(tbdm)
    probabilities = q_transposed.dot(tbdm)
    probabilities = probabilities.toarray()

    indexes = np.arange(n)
    probabilities = list(zip(indexes, probabilities[0]))
    probabilities.sort(key=lambda x:x[1], reverse=True)

    return probabilities

def make_svd(tbdm, m, num_of_iterations):
    u, s, vt = svds(tbdm, num_of_iterations)
    ut = u.transpose()
    tbdm = None
    del (tbdm)
    gc.collect()

    result=csr_matrix((m, n))
    for i in range(num_of_iterations):
        u1 = ut[i].reshape((m, 1))
        v1 = vt[i].reshape((1, n))
        matrix = s[i] * u1.dot(v1)
        result = result + matrix
        print(i)

    matrix = None
    del(matrix)
    gc.collect()

    for j in range(n):
        length_to_power = 0

        for i in range(m):
            length_to_power = length_to_power + result[i, j] ** 2

        length_to_power = math.sqrt(length_to_power)

        for i in range(m):
            result[i, j] = result[i,j] / length_to_power

    result = csr_matrix(result)
    name_svd = f'svd_sparse_{num_of_iterations}.npz'
    scipy.sparse.save_npz(name_svd, result)


#create_dictionary()
#create_links_dictionary()
dic1 = open("dictionary.txt", 'r', encoding='utf-8').read()
dictionary = ast.literal_eval(dic1)
m = len(dictionary)
dic2 = open("links_dictionary.txt", 'r', encoding='utf-8').read()
links_dictionary = ast.literal_eval(dic2)

#create_term_by_document_matrix(dictionary, m)
tbdm = scipy.sparse.load_npz('tbdm_sparse.npz')

make_svd(tbdm, m, k)          
name = f'svd_sparse_{k}.npz'
svd = scipy.sparse.load_npz(name)

incorrect = True

while(True):
    while(incorrect):
        incorrect = False
        print("Type quit to quit")
        print("Number of words in query must be between 2 and 5")
        q = input("Enter query: ")
        if(q == "quit"):
            exit(1)

        for word in q.split():
            stemmed_word = ps.stem(word)
            if(stemmed_word not in stop_words):
                if (stemmed_word not in dictionary):
                    print(f'{word} not in dictionary')
                    incorrect = True
                    break

        if(len(q.split()) > 5 or len(q.split()) < 2):
            incorrect = True

    incorrect = True

    while(True):
        l = input("Number of documents to be printed: ")
        l = int(l)
        if(l > 0):
            break
        print("It must be greater than 0")

    prob = calculate_prob_matrix(tbdm, dictionary, m, q)
    #prob_svd = calculate_prob_matrix(svd, dictionary, m, q)


    print('Probabilities from sparse tbdm')

    for i in range(l):
        tuple = prob[i]
        print(tuple)
        print(links_dictionary[tuple[0]])

    #print('Probabilities from svd')

    #for i in range(l):
     #   tuple = prob_svd[i]
      #  print(tuple)
       # print(links_dictionary[tuple[0]])






