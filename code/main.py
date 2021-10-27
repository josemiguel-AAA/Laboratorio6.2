import os
import codecs
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.util import tokenwrap

nltk.download('punkt')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

docPath = os.getcwd() + "\documentos"

# Letura de lista de stopwords
with open(os.getcwd() + "\stop_list.txt", 'r', encoding='utf-8') as file:
    stoplist = [line.lower().strip() for line in file]
stoplist += ['.', '?', ',', '-', '«', '»', '(', ')', '"', '\'', ':', ';', '!', '¡', '¿', '`', '``', '\'\'']

# Eliminacion de stopwords
def clean(list):
    palabras_limpias = list[:]
    for token in list:
        if token in stoplist:
            palabras_limpias.remove(token)
    return palabras_limpias

# Reduccion de palabras
def stem(list):
    stemmer = SnowballStemmer('spanish')
    palabras_reducidas = []
    for token in list:
        palabras_reducidas.append(stemmer.stem(token))
    return palabras_reducidas

# Procesamiento de documentos
def readDocuments():
    docs = {}
    cont = 1
    for filename in os.listdir(docPath):
        with open(os.path.join(docPath, filename), 'r', encoding='utf-8') as f:
            texto = f.read()
            palabras = nltk.word_tokenize(texto.lower())
            palabras = clean(palabras)
            palabras = stem(palabras)
            docs[cont] = palabras
            cont += 1
    return docs

# Clase del indice invertido
class InvertedIndex:
    filename = ""
    index = {}
    
    def __init__(self, filename):
        self.filename = filename
        self.createIndex()

    def createIndex(self):
        docs = readDocuments()
        tokenFreq = []
        tokens = []
        for doc in docs:
            for token in docs[doc]:
                tokens.append(token)
        
        tokensSet = set(tokens.copy())
        for token in tokensSet:
            tokenFreq.append([token, tokens.count(token)])

        tokenFreq = sorted(tokenFreq, key = lambda x:(-x[1], x[0]), reverse=True)
        topTokens = tokenFreq[len(tokenFreq)-500:len(tokenFreq)]
        topTokens = sorted(topTokens)

        for token in topTokens:
            docIDs = []
            for doc in docs:
                if token[0] in docs[doc]:
                    docIDs.append(doc)
            self.index[token[0]] = [token[1], docIDs]
            
        self.write()

    def write(self):
        f = open(os.path.join(os.getcwd(), self.filename), 'w', encoding='utf-8')
        for token in self.index:
            s = ""
            for docID in self.index[token][1]:
                s = s + str(docID) + ','
            f.write(token + ':' + s[:-1] + '\n')
        f.close()

    def L(self, token):
        if isinstance(token, list):
            return token
        stemmer = SnowballStemmer('spanish')
        newToken = stemmer.stem(token)
        if newToken in self.index:
            return self.index[newToken][1]
        return "Word was not found"

    def AND(self, token1, token2):
        list1 = self.L(token1) + [-1]
        list2 = self.L(token2) + [-1]
        p1 = 0
        p2 = 0
        res = []

        while list1[p1] != -1 and list2[p2] != -1: 
            if list1[p1] == list2[p2]:
                res.append(list1[p1])
                p1 += 1
                p2 += 1
            else:
                if list1[p1] < list2[p2]:
                    p1 += 1
                else:
                    p2 += 1
        return res

    def OR(self, token1, token2):
        list1 = self.L(token1) + [-1]
        list2 = self.L(token2) + [-1]
        p1 = 0
        p2 = 0
        res = []

        while list1[p1] != -1 and list2[p2] != -1: 
            if list1[p1] == list2[p2]:
                res.append(list1[p1])
                p1 += 1
                p2 += 1
            else:
                if list1[p1] < list2[p2]:
                    res.append(list1[p1])
                    p1 += 1
                else:
                    res.append(list2[p2])
                    p2 += 1

        while list1[p1] != -1:
            res.append(list1[p1])
            p1 += 1

        while list2[p2] != -1:
            res.append(list2[p2])
            p2 += 1
            
        return res
        
    def AND_NOT(self, token1, token2):
        list1 = self.L(token1) + [-1]
        list2 = self.L(token2) + [-1]
        p1 = 0
        p2 = 0
        res = []

        while list1[p1] != -1 and list2[p2] != -1: 
            if list1[p1] == list2[p2]:
                p1 += 1
                p2 += 1
            else:
                if list1[p1] < list2[p2]:
                    res.append(list1[p1])
                    p1 += 1
                else:
                    p2 += 1
        return res
        
# Prueba
index = InvertedIndex("index.txt")

print("\nCondulta 1:")
print("-----------")
print("Gandalf:", index.L("Gandalf"))
print("Frodo:", index.L("Frodo"))
print("Gondor:", index.L("Gondor"))
print("(Gandalf AND Frodo) AND NOT Gondor: ", index.AND_NOT(index.AND("Gandalf", "Frodo"), "Gondor"))

print("\nCondulta 2:")
print("-----------")
print("Orthanc:", index.L("Orthanc"))
print("Anillo:", index.L("Anillo"))
print("Nazgûl:", index.L("Nazgûl"))
print("Orthanc OR (Anillo AND NOT Nazgûl): ", index.OR("Orthanc", index.AND_NOT("Anillo", "Nazgûl")))

print("\nCondulta 3:")
print("-----------")
print("Merry:", index.L("Merry"))
print("Hobbit:", index.L("Hobbit"))
print("Gimli:", index.L("Gimli"))
print("(Merry AND Hobbit) OR Gimli: ", index.OR(index.AND("Merry", "Hobbit"), "Gimli"))