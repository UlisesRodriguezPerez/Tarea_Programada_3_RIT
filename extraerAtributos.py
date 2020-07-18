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
from lectorDeArchivos import eliminarStopWords

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
    a = eliminarStopWords(str(a))   #Elimina los stopWords de cada body
    bodies.append(a)

    


for b in soup.findAll("topics"):
    topics.append(b)
    

for item in soup.findAll('REUTERS'):
    tags.append(item['TOPICS'])

# print("\n\n\n\n\n\n\n\n\nBodies:\n",bodies)
# print("\n\n\n\n\n\n\n\n\nTopics:\n",topics)
# print("\n\n\n\n\n\n\n\n\nTags:\n",tags)