import io 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

# def extraerColeccion():
#     f = open("reut2-001.sgm", "r")
#     coleccion = f.readlines()             Prueba 
#     for a in coleccion:
#         print (a)
#     # print(coleccion)
    


def eliminarStopWords(texto):

    stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any",
                "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
                "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing",
                "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
                "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
                "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", 
                "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once",
                "only", "or","other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd",
                "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", 
                "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
                "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", 
                "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", 
                "whom", "why", "why's","with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", 
                "yours", "yourself"] 
    #file1 = open("textoDePrueba.txt","r")
    #line = file1.read() #lee el archivo en secuencia.
    textoSinStopWords = ""
    separador = " "
    palabrasDelTexto = texto.split(separador) #separa las plaabras del texto.
    for palabra in palabrasDelTexto: 
        if not palabra in stop_words: 
            textoSinStopWords += palabra + " "
            #appendFile = open('textoSinStopWords.txt','a') 
            #appendFile.write(" "+palabra) 
           #appendFile.close() 
        # else:
        #     print(palabra)
        
    return textoSinStopWords

def eliminarComasEntreNumeros(texto):    
    import re
    nuevoTexto = re.sub(',(?=[^\d+]*\d+[^\d+]*(?:\d+[^\d+]*\d+[^\d+]*)*$)',"", texto)   #Expresión regular que elimina las comas entre puntos.
    return nuevoTexto

# eliminarStopWords()
# extraerColeccion()
# eliminarComasEntreNumeros(texto)