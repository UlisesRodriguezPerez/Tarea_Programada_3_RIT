import arff
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


def leerColeccion():
    textoTotal =""

    with open('reut2-001.sgm', 'r') as inF:
        for line in inF:
            texto = re.sub("[^0-9a-zA-Z<>/\s=!-\"\"]+","", line)#Pendinete ver cuales son permitidos
            textoTotal += texto 
    # print(textoTotal)
    soup = BeautifulSoup(textoTotal,"html.parser")

    bodies = list()
    topics = list()
    tags = list()

    for a in soup.findAll("body"):
        a = eliminarStopWords(str(a))       #Elimina los stopWords de cada body.
        a = eliminarComasEntreNumeros(a)    #Elimina las comas entre números.
        bodies.append(a)
        
    for b in soup.findAll("topics"):
        topics.append(b)        
        
    for item in soup.findAll('reuters'):
        print(item)
        
        tags.append(item['title'])

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

# print("\n\n\n\n\n\n\n\n\nBodies:\n",bodies)
# print("\n\n\n\n\n\n\n\n\nTopics:\n",topics)
# print("\n\n\n\n\n\n\n\n\nTags:\n",tags)
