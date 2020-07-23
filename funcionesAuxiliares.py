# coding=<UTF-8>

import io 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from timeit import default_timer
import operator
import re

# def extraerColeccion():
#     f = open("reut2-001.sgm", "r")
#     coleccion = f.readlines()             Prueba 
#     for a in coleccion:
#         print (a)
#     # print(coleccion)
    


def eliminarStopWords(texto):# Funcion para eliminar stopWords, pendiente hacerla de manera que  lea de un txt.

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
    palabrasDelTexto = texto.split(separador) #separa las palabras del texto.
    for palabra in palabrasDelTexto: 
        if not palabra in stop_words: 
            textoSinStopWords += palabra + " "

    return textoSinStopWords


def eliminarComasEntreNumeros(texto): 
    nuevoTexto = re.sub('(?<=\\d),(?=\\d)',"", texto)   #Expresión regular que elimina las comas entre numeros.
    return nuevoTexto



def generarClasesTxt(Clases, listaArticulos, minNc): #Esta funcion genera el txt de clases y llama a la funcion para generar el txt de Docs. Deben de ser complementarias.
    inicio = default_timer()
    topicsAceptados = dict()             #El diccionario de topics aceptados es para saber cuales si son aceptados por minNc
    Clases = sorted(Clases.items(), key=operator.itemgetter(1), reverse = True)
    with open("clases.txt","w",encoding="UTF-8") as archivoClases:
        for item in Clases:
            if item[1] < minNc:
                break
            else:
                archivoClases.write(str(item[0]) + "\t" + str(item[1]) + "\n")
                topicsAceptados[item[0]] = 1
    final = default_timer()
    print( "Tardó ", final-inicio, " segundos en generar 'clases.txt'.")
    generarDocsTxt(topicsAceptados,listaArticulos,minNc)  

    #inicio = default_timer()
    # Clases = sorted(Clases.items(), key=operator.itemgetter(1), reverse = True)
    # with open("clases.txt","w",encoding="UTF-8") as archivoClases:
    #     for item in Clases:
    #         if item[1] < minNc:
    #           Clases.pop(item[0])
    #         else:
    #             archivoClases.write(str(item[0]) + "\t" + str(item[1]) + "\n")
    # final = default_timer()
    # print( "Tardó ", final-inicio, " segundos en generar 'clases.txt'.")
    # generarDocsTxt(Clases,listaArticulos,minNc)      



def generarDocsTxt(topicsAceptados,listaDeArticulos,minNc):
    inicio = default_timer()
    listaDeArticulosPermitidos = []
    with open("docs.txt","w",encoding="UTF-8") as archivoDocs:
        for articulo in listaDeArticulos:
            if articulo[0] in topicsAceptados: #Si el articulo se encuentra en el dicc de topics aceptados, significa que también está en las clases restringidas.
                archivoDocs.write(str(articulo[1]) + "\t" + articulo[0] + "\n")   #El formato es (ID, Clase a la que pertenece)
                listaDeArticulosPermitidos.append(articulo)
    final = default_timer()
    print( "Tardó ", final-inicio, " segundos en generar 'docs.txt'.")
    generarDiccTxt(listaDeArticulosPermitidos)



def generarDiccTxt(listaDeArticulosPermitidos):
    inicio = default_timer()
    listaDeDiccionarios = generarListaDeDiccionarios(listaDeArticulosPermitidos)  #Se llama la función "generarListaDeDiccionarios" para nada más proceder a la comparación.
    diccionarioGeneral = generarDiccionarioGeneral(listaDeArticulosPermitidos)  #Genera un diccionario, con todas las palabras de la colección.
    listaDePalabras = []

    for palabra in diccionarioGeneral: #Recorre todas las palabras de la colección(sección body).
        contadorDeArticulos = 0
        contador_ni = 0
        while contadorDeArticulos < len(listaDeDiccionarios):   #recorre la lista de diccionarios, uno para cada artículo y contar el "ni".
            if palabra in listaDeDiccionarios[contadorDeArticulos]: # Solo identifica si la palabra esta, no cuantas veces aparece en cada documento.
                contador_ni += 1
            contadorDeArticulos +=1
        listaDePalabras.append([palabra,contador_ni])   #Se agregan a una lista, para despues ordenarla de mayor a menor.

    listaDePalabras = sorted(listaDePalabras,key=operator.itemgetter(1), reverse = True)    #Se ordena la lista con respecto a caantidad de "ni" de cada palabra.

    with open("dicc.txt","w",encoding="UTF-8") as archivoDiccs: #Se genera el archivo de texto "dics.txt"
        for palabra in listaDePalabras:
            palabraFiltrada = re.sub("[^a-z\\d+.\\/]","",palabra[0])
            archivoDiccs.write(str(palabraFiltrada) + "\t" + str(palabra[1]) + "\n") 
    
    final = default_timer()
    print( "Tardó ", final-inicio, " segundos en generar 'dicc.txt'.")

        
    

def generarDiccionarioGeneral(listaDeArticulosPermitidos):  #Genera un diccionario para toda la colección.
    diccionarioGeneral = dict()
    for articulo in listaDeArticulosPermitidos:
        articulo = articulo[2].lower()         #Pasa a minúsculas.
        articulo = articulo.split()
        
        for palabra in articulo:
            if palabra in diccionarioGeneral:
                valor = diccionarioGeneral[palabra]
                diccionarioGeneral[palabra] = valor + 1 
            else:
                diccionarioGeneral[palabra] = 1
    return diccionarioGeneral



def generarListaDeDiccionarios(listaDeArticulosPermitidos):
    listaDeDiccionarios = [] #La lista de diccionarios contiene el diccionrio de cada artículo, para facilitar el conteo del "ni" de cada término.
    for articulo in listaDeArticulosPermitidos:
        nuevoDicc = generarDiccionario(articulo[2])
        listaDeDiccionarios.append(nuevoDicc)
    return listaDeDiccionarios



def generarDiccionario(articulo):   #Genera el diccionario del artículo que se le de por parametro.
    diccionarioDelArticulo = dict()
    articulo = articulo.lower()        #Se pasan a minúsculas.
    articulo = articulo.split()        #Se separa en palabras.
    for palabra in articulo:
        if palabra in diccionarioDelArticulo:
            valor = diccionarioDelArticulo[palabra]
            diccionarioDelArticulo[palabra] = valor+1
        else:
            diccionarioDelArticulo[palabra] = 1
    return diccionarioDelArticulo  



        

# eliminarStopWords()
# extraerColeccion()
# eliminarComasEntreNumeros("Hola como estas, te debo 800,00.20 colones")
