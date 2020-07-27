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

def leerColeccion(archivo, minNc):
    inicio = default_timer()
    textoTotal =""
    listaArticulos = []

    with open(archivo, 'r') as inF:
        for line in inF:
            texto = re.sub("[^0-9a-zA-Z<>/\\s=!-\"\",.]+"," ", line)#Pendinete ver cuales son permitidos
            textoTotal += texto 

    soup = BeautifulSoup(textoTotal,"html.parser")
    a= 0
    Clases = dict()
    for articulo in soup.findAll('reuters'):
        ID = articulo["newid"]
        if articulo["topics"] == "YES" and articulo.topics.text != '' and articulo.body != None:
            Topics = articulo.topics.text
            #print(Topics)                                            #PENDIENTE OBTENER SOLO UHN TOPICS SIEMPRE.
            Body = articulo.body.text
            if Body[len(Body)-1] == '3':
                Body = Body[:-1]
            Body = eliminarStopWords(Body)
            
            if a == 2:
                break
            a+=1
            if Topics in Clases:
                valor = Clases[Topics]
                Clases[Topics] = valor+1
            else:
                Clases[Topics] = 1
                
            HayTopics = articulo["topics"]

            # print(Topics)
            # print(ID)
            # print (Body)
            # print(HayTopics)

            listaArticulos.append([Topics,ID,Body,HayTopics])
    final = default_timer()
    print( "Tardó ", final-inicio, " segundos en procesar la colección.")
    generarClasesTxt(Clases, listaArticulos, minNc)
    
