# import arff
from xml.etree import ElementTree
import re
from io import StringIO
from bs4 import BeautifulSoup 
import bs4                      #pip3 install bs4
from unicodedata import normalize
import requests                 #pip install requests
import urllib.request
import string
import codecs
from funcionesAuxiliares import eliminarStopWords, eliminarComasEntreNumeros


def leerColeccion(archivo):
    textoTotal =""
    ListaArticulos = []


    with open(archivo, 'r') as inF:
        for line in inF:
            texto = re.sub("[^0-9a-zA-Z<>/\\s=!-\"\"]+","", line)#Pendinete ver cuales son permitidos
            textoTotal += texto 

    soup = BeautifulSoup(textoTotal,"html.parser")

    a = 0
    Clases = dict()
    for articulo in soup.findAll('reuters'):
        ID = articulo["newid"]
        if articulo["topics"] == "YES" and articulo.topics.text != '' and articulo.body != None:
            Topics = articulo.topics.text
            Body = articulo.body.text
            if Body[len(Body)-1] == '3':
                Body = Body[:-1]
            
            if Topics in Clases:
                valor = Clases[Topics]
                print ("VALOR: ", valor)
                Clases[Topics] = valor+1
            else:
                Clases[Topics] = 1
                
            HayTopics = articulo["topics"]

            print(Topics)
            print(ID)
            print (Body)
            print(HayTopics)

        a+=1
        if a == 10:
            break
    with open("clases.txt","w",encoding="UTF-8") as archivoClases:
        for item in Clases:
            archivoClases.write(item+"\t"+str(Clases[item])+"\n")
    print (Clases.items())
    

    


    # for b in soup.findAll("topics"):
    #     topics.append(b)        

    

# for a in soup.findAll("body"):
#         a = eliminarStopWords(str(a))       #Elimina los stopWords de cada body.
#         a = eliminarComasEntreNumeros(a)    #Elimina las comas entre números.
#         bodies.append(a)

    # print("\n\n\n\n\n\n\n\n\nBodies:\n",bodies)
    # print("\n\n\n\n\n\n\n\n\nTopics:\n",topics)
    # print("\n\n\n\n\n\n\n\n\nTags:\n",tags)

# def get_articles(file_path):
#       import bs4
#       import tensorflow as tf

#       data = tf.gfile.GFile(file_path).read()
#       soup = bs4.BeautifulSoup(data, "html.parser")
#       articles = []
#       for raw_article in soup.find_all('reuters'):
#         article = {
#             'title': get_title(raw_article),
#             'content': get_content(raw_article),
#             'topics': get_topics(raw_article),
#         }
#         if None not in article.values():
#           if [] not in article.values():
#             articles.append(article)
#       return articles
