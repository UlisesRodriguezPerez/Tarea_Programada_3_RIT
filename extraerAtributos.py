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
import operator
from timeit import default_timer
import codecs
from funcionesAuxiliares import *

def leerColeccion(archivo):
    inicio = default_timer()
    Body = Topics = Tags = []
    Datos = [Body, Topics, Tags]
    textoTotal =""
    Articulos = []
    stopwords = cargarStopWords("stopWords.txt")

    with open(archivo, 'r') as contenido:
        for line in contenido:
            texto = re.sub("[^0-9a-zA-Z<>/\\s=!.]+","", line) #Pendiente ver cuales son permitidos
            textoTotal += texto 

    soup = BeautifulSoup(textoTotal,"html.parser")

    Clases = dict()
    for articulo in soup.findAll('reuters'):    # Se extraen los datos de cada articulo
        ID = articulo["newid"]
        if articulo["topics"] == "YES" and articulo.topics.text != '' and articulo.body != None:
            
            Body = articulo.body.text
            Body = filtrarTexto(Body, stopwords)
            Body = Body.split()

            Topic = articulo.topics.d.string

            if Topic in Clases:
                valor = Clases[Topic]
                Clases[Topic] = valor+1
            else:
                Clases[Topic] = 1
                
            HayTopics = articulo["topics"]

            Articulos.append([Topic,ID,Body,HayTopics])
    final = default_timer()
    print( "Tardó ", final-inicio, " segundos en procesar la colección.")

    return Articulos, Clases
    
    
