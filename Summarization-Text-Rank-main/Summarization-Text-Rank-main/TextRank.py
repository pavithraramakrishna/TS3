from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import re

class TextRank():

    def __init__(self, document):
        self.__document = document
        self.__sentence = []
        self.__raw_sentence = []
        self.__set_raw_sentence()
        self.__break_into_token()
        self.__stop_word()
        self.__stemming()
        self.__ranking()
    

    def __set_raw_sentence(self):
        document = re.sub("<[^>]+>", "", self.__document).strip()
        self.__raw_sentence = sent_tokenize(document)
    
    def __break_into_token(self):
        document = re.sub("<[^>]+>", "", self.__document).strip() #Remove HTML Tag
        document = document.lower() #Lowercase
        sentence = sent_tokenize(document) #Tokenize the sentence
        for s in sentence:
            s = re.sub(r'[^\w\s]','',s) #Remove punctuation
            s = re.sub(r'\w*\d\w*','',s) #Remove number
            if s != None:
                self.__sentence.append(s)
            else:
                self.__sentence.append(".")
        self.__word = [word_tokenize(word) for word in self.__sentence]
    
    def __stop_word(self):
        #nltk.download('stopwords') #Uncomment to download package
        english_stop = set(stopwords.words('english'))
        self.__word = [[w for w in word if w not in english_stop] for word in self.__word]

    def __stemming(self):
        self.__word = [[PorterStemmer().stem(w) for w in word] for word in self.__word]
    #### end data cleansing ####

    #### start TextRank algorithm ####
    def __sentence_similarity(self, sentence1, sentence2):
        sentence1 = [word for word in sentence1]
        sentence2 = [word for word in sentence2]
        all_words = list(set(sentence1+sentence2))
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)
        for w in sentence1:
            vector1[all_words.index(w)] += 1
        for w in sentence2:
            vector2[all_words.index(w)] += 1
        return 1 - cosine_distance(vector1, vector2)

    def __similarity_matrix(self):
        similarity_matrix = np.zeros((len(self.__word), len(self.__word)))
        for index1 in range(len(self.__word)):
            for index2 in range(len(self.__word)):
                if index1 == index2:
                    continue
                similarity_matrix[index1][index2] = self.__sentence_similarity(self.__word[index1], self.__word[index2])
        return similarity_matrix
    
    def __ranking(self):
        similarity_graph = nx.from_numpy_array(self.__similarity_matrix())
        score = nx.pagerank(similarity_graph)
        ranked_sentence = sorted(((score[i],s) for i,s in enumerate(self.__raw_sentence)), reverse=True)
        self.__ranked_sentence = ranked_sentence
    
    def summarize(self, top_sentence = 4):
        summarized = ""
        for i in range(top_sentence):
            summarized += str(self.__ranked_sentence[i][1])+" "
            print(f"Word similarity: {self.__ranked_sentence[i][0]}")
            print(f"Represented sentence: {self.__ranked_sentence[i][1]}")
        return summarized

    #### End TextRank Algorithm ####