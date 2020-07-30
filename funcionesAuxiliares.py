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
                "yours", "yourself",""] 

def eliminarStopWords(texto):# Funcion para eliminar stopWords, pendiente hacerla de manera que  lea de un txt.

    #file1 = open("textoDePrueba.txt","r")
    #line = file1.read() #lee el archivo en secuencia.
    textoSinStopWords = ""
    separador = " "
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9,.]"," ",texto)
    texto = texto.replace(",", "")
    texto = eliminarPuntosDelTexto(texto)    #TODO Pendiente cambiar función por dejar  punto entre números.
    palabrasDelTexto = texto.split(separador) #separa las palabras del texto.
    for palabra in palabrasDelTexto: 
        
        if not palabra in stop_words: 
            textoSinStopWords += palabra + " "
        
    return textoSinStopWords


def eliminarPuntosDelTexto(texto): 
    nuevoTexto = re.sub("(?<!\\d)\\.(?=\\d)|(?<=\\d)\\.(?!\\d)|(?<!\\d)\\.(?!\\d)","", texto)   #Expresión regular que elimina las comas entre numeros.
    return nuevoTexto


def generarClasesTxt(Clases, listaArticulos, minNc,minNi): #Esta funcion genera el txt de clases y llama a la funcion para generar el txt de Docs. Deben de ser complementarias.
    inicio = default_timer()
    topicsAceptados = dict()             #El diccionario de topics aceptados es para saber cuales si son aceptados por minNc
    Clases = sorted(Clases.items(), key=operator.itemgetter(1), reverse = True)
    nuevoDiccionarioDeClases = dict() #ESte diccionario será usado para calcular la diferencia de cada termino, restando el total de apariciones de esa 
                                    #clase - la cantidad de clases en las que apareció la palabra.

    with open("clases.txt","w",encoding="UTF-8") as archivoClases:
        for item in Clases:
            if item[1] < minNc:
                break
            else:
                archivoClases.write(str(item[0]) + "\t" + str(item[1]) + "\n")
                topicsAceptados[item[0]] = 1
                nuevoDiccionarioDeClases[item[0]] = item[1]     #Diccionario con las clases que se piden por parámetro.
    #print(nuevoDiccionarioDeClases  )
    final = default_timer()
    print( "Tardó ", final-inicio, " segundos en generar 'clases.txt'.")
    generarDocsTxt(topicsAceptados,listaArticulos,minNc,minNi,nuevoDiccionarioDeClases)  

    #SUGERENCIA
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



def generarDocsTxt(topicsAceptados,listaDeArticulos,minNc,minNi,nuevoDiccionarioDeClases):
    inicio = default_timer()
    listaDeArticulosPermitidos = []
    with open("docs.txt","w",encoding="UTF-8") as archivoDocs:
        for articulo in listaDeArticulos:
            if articulo[0] in topicsAceptados: #Si el articulo se encuentra en el dicc de topics aceptados, significa que también está en las clases restringidas.
                archivoDocs.write(str(articulo[1]) + "\t" + articulo[0] + "\n")   #El formato es (ID, Clase a la que pertenece)
                listaDeArticulosPermitidos.append(articulo)
    final = default_timer()
    print( "Tardó ", final-inicio, " segundos en generar 'docs.txt'.")
    generarDiccTxt(listaDeArticulosPermitidos,minNi,nuevoDiccionarioDeClases)



def generarDiccTxt(listaDeArticulosPermitidos,minNi,nuevoDiccionarioDeClases):
    inicio = default_timer()
    #listaDeDiccionarios = generarListaDeDiccionarios(listaDeArticulosPermitidos)  #Se llama la función "generarListaDeDiccionarios" para nada más proceder a la comparación.
    diccionarioGeneralAndDatosParaGI = generarDiccionarioGeneralAndDatosParaGI(listaDeArticulosPermitidos,nuevoDiccionarioDeClases)  
    diccionarioGeneral = diccionarioGeneralAndDatosParaGI[0]   #Genera un diccionario,con todas las palabras de la colección.
    infoGI = diccionarioGeneralAndDatosParaGI[1]
    listaDePalabras = []

    for palabra in diccionarioGeneral: #Recorre todas las palabras de la colección(sección body).
        contadorDeArticulos = 0
        contador_ni = 0
        while contadorDeArticulos < len(listaDeArticulosPermitidos):   #recorre la lista de diccionarios, uno para cada artículo y contar el "ni".
            if palabra in listaDeArticulosPermitidos[contadorDeArticulos][2]: # Solo identifica si la palabra esta, no cuantas veces aparece en cada documento.
                contador_ni += 1
            contadorDeArticulos +=1
        if contador_ni < minNi:
            break
        listaDePalabras.append([palabra,contador_ni])   #Se agregan a una lista, para despues ordenarla de mayor a menor.

    listaDePalabras = sorted(listaDePalabras,key=operator.itemgetter(1), reverse = True)    #Se ordena la lista con respecto a caantidad de "ni" de cada palabra.

    with open("dicc.txt","w",encoding="UTF-8") as archivoDiccs: #Se genera el archivo de texto "dics.txt"
        for palabra in listaDePalabras:
            palabraFiltrada = re.sub("[^a-z\\d+.\\/]","",palabra[0])
            if palabraFiltrada not in stop_words:
                archivoDiccs.write(str(palabraFiltrada) + "\t" + str(palabra[1]) + "\n") 


        #TXT DE PRUEBA; PARA VISUALIZAR LAS PALABRAS Y SUS CALCULOS RESPECTIVOS:**************************************************************************
        #*******************************************************************************************************************************+
    with open("infoGanaciaInformacion.txt","w",encoding="UTF-8") as archivoInfoGI: 
        
        for contPalabras in range(len(infoGI)): #Recorre las palabras.
            archivoInfoGI.write("Palabra: " + infoGI[contPalabras][0] + "\n")    #PALABRA.
            #print(infoGI[contPalabras][0])
            for contClasesPorPalabra in infoGI[contPalabras][1]:   #Recorre las clases de cada palabra.
                archivoInfoGI.write("\t\tClase:")
               
                archivoInfoGI.write(str(contClasesPorPalabra) + "\n\t\t\t" + str("Info de la clase:") + "\n" + "\t\t\t\t\t" + str(infoGI[contPalabras][1][contClasesPorPalabra][0])
                + "\t\t" + str(infoGI[contPalabras][1][contClasesPorPalabra][1]) + "\t\t" + str(infoGI[contPalabras][1][contClasesPorPalabra][2])
                + "\n")          #escribe -> (clase , itermi-i , -itermi-i , totalDeClase)
                    
            #archivoInfoGI.write(str(infoGI[0][1][info]) + "\n")
    #print(infoGanaciaInformacion)
    final = default_timer()
    print( "Tardó ", final-inicio, " segundos en generar 'dicc.txt'.")

        
    

def generarDiccionarioGeneralAndDatosParaGI(listaDeArticulosPermitidos,nuevoDiccionarioDeClases):  #Genera un diccionario para toda la colección.
    diccionarioGeneral = dict()
    listaConTodaLaInformacion = []       #Esta lista contiene toda la informacion para el calculo de ganancia de información, cada indice es una palabra..

    for articulo in listaDeArticulosPermitidos:
        articulo = articulo[2].lower()         #Pasa a minúsculas.
        articulo = articulo.split()
        
        for palabra in articulo:
            if palabra in diccionarioGeneral:
                valor = diccionarioGeneral[palabra]
                diccionarioGeneral[palabra] = valor + 1 
            else:
                diccionarioGeneral[palabra] = 1
                listaConTodaLaInformacion.append(prepararInformacionParaGI(palabra,listaDeArticulosPermitidos,nuevoDiccionarioDeClases))

    datos = [diccionarioGeneral,listaConTodaLaInformacion]  #LA FUNCIÓN "generarDiccionariosGeneralAndDatosGI", RETORNA EL DICCIONARIO GENERAL PARA EL CÁLCULO
                                                            #DEL "dicc.txt" Y UNA LISTA CON TODAS LAS PALABRAS Y SUS DATOS PARA PROCEDER CON
                                                            #EL CÁLCULO DE GANACIA DE INFORMACIÓN. (SIMPLEMENTE SERÍA RECORRER LA LISTA DE PALABRAS
                                                            # Y SU RESPECTIVO DICCIONARIO DE CLASES Y VALORES).
    return  datos
    

def prepararInformacionParaGI(palabra, listaDeArticulosPermitidos, nuevoDiccionarioDeClases):

    
    diccionarioPorPalabra = dict()  
    existePalabraEnArticulo = False

    for counterClases in range(len(listaDeArticulosPermitidos)):

        if palabra in listaDeArticulosPermitidos[counterClases][2]: #El indice 2 es el body del artículo.
            existePalabraEnArticulo = True
            clase = listaDeArticulosPermitidos[counterClases][0]

            if clase in diccionarioPorPalabra:    #EL DICCIONARIO POR PALABRA LLEVA EL SIGUIENTE ORDEN 
                                                #-> {clase: [termi-i , -termi-i, total], ... clase: [termi-i , -termi-i, total]}
                total = nuevoDiccionarioDeClases[clase] 
                valor = diccionarioPorPalabra[clase]
                valor = valor[0] + 1
                diccionarioPorPalabra[clase] = [valor ,total-valor,total] 
            else:
                total = nuevoDiccionarioDeClases[clase]
                diccionarioPorPalabra[clase] = [1, total - 1, total]
    return [palabra,diccionarioPorPalabra]
                
            
        
    
    listaConTodaLaInformacion.append([palabra,diccionarioPorPalabra])
    # print(listaConTodaLaInformacion[0])
    # print(total)
















