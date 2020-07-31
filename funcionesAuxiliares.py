# coding=<UTF-8>

import io 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from timeit import default_timer
import operator
import re
import math

def cargarStopWords(nombreArchivo):
	# Se abre el archivo de stop words
	with open(nombreArchivo,"r") as archivo:
		contenido = archivo.read()          #lee todo el archivo.
	stopwords = contenido.split(",")
	for i in range(0,len(stopwords)):
		stopwords[i] = stopwords[i].strip("\n")
	stopwords.append("")

	return stopwords

def eliminarStopWords(texto, stopwords):# Funcion para eliminar stopWords
	textoSinStopWords = ""  
	palabrasDelTexto = texto.split(" ")
   
	# Se quitan los stop words
	for palabra in palabrasDelTexto:     
		if not palabra in stopwords: 
			textoSinStopWords += palabra + " "
		
	return textoSinStopWords

def dejarPuntosSoloEnNumeros(texto): 
	texto = re.sub(r"[^a-z0-9,.\"\'']"," ",texto)
	texto = texto.replace(",", "")
	texto = texto.replace("\'","")
	texto = texto.replace("\"","")
	nuevoTexto = re.sub("(?<!\\d)\\.(?=\\d)|(?<=\\d)\\.(?!\\d)|(?<!\\d)\\.(?!\\d)","", texto)   #Expresión regular que elimina las comas entre numeros.
	return nuevoTexto

def filtrarTexto(texto, stopwords):
	# Se quita el 3 al final de los articulos
	if texto[len(texto)-1] == '3':    
		texto = texto[:-1]
	texto = texto.lower()
	# Se pasa todo a minuscula deja [a-z0-9] y permite puntos solo entre numeros
	texto = dejarPuntosSoloEnNumeros(texto)
	# Quita los stop words
	texto = eliminarStopWords(texto, stopwords)
	return texto

def generarClasesTxt(Clases, minNc): #Esta funcion genera el txt de clases y llama a la funcion para generar el txt de Docs. Deben de ser complementarias.
	inicio = default_timer()
	#topicsAceptados = []             #El diccionario de topics aceptados es para saber cuales si son aceptados por minNc
	ClasesOrdenadas = sorted(Clases.items(), key=operator.itemgetter(1), reverse = True)	#Es una lista, no un diccionario
	ClasesMinNC = dict() #Este diccionario será usado para calcular la diferencia de cada termino, restando el total de apariciones de esa 
									  #clase - la cantidad de clases en las que apareció la palabra.
	totalDeClases = 0
	with open("clases.txt","w",encoding="UTF-8") as archivoClases:
		for clase in ClasesOrdenadas:
			if clase[1] <= minNc:
				break
			else:
				totalDeClases += clase[1]
				archivoClases.write(str(clase[0]) + "\t" + str(clase[1]) + "\n")
				#topicsAceptados.append(clase[0])
				ClasesMinNC[clase[0]] = clase[1]    #Diccionario con las clases que se piden por parámetro.

	final = default_timer()
	print( "Tardó ", final-inicio, " segundos en generar 'clases.txt'.")
	return ClasesMinNC, totalDeClases
		

def generarDocsTxt(l_Documentos, d_Clases):
	inicio = default_timer()
	l_DocumentosPermitidos = []
	with open("docs.txt","w",encoding="UTF-8") as archivoDocs:
		for articulo in l_Documentos:
			if articulo[0] in d_Clases.keys(): #Si el articulo se encuentra en la lista de llaves del dict de clases aceptadas, significa que también está en las clases restringidas.
				archivoDocs.write(str(articulo[1]) + "\t" + articulo[0] + "\n")   #El formato es (ID, Clase a la que pertenece)
				l_DocumentosPermitidos.append(articulo)
	final = default_timer()
	print( "Tardó ", final-inicio, " segundos en generar 'docs.txt'.")
	return l_DocumentosPermitidos


def generarDiccTxt(l_Documentos,d_Clases,minNi):
	inicio = default_timer()
	#listaDeDiccionarios = generarListaDeDiccionarios(listaDeArticulosPermitidos)  #Se llama la función "generarListaDeDiccionarios" para nada más proceder a la comparación.
	s_General, d_TablasGI = generarConjuntoPalabrasAndDatosParaGI(l_Documentos,d_Clases) 
	d_Palabras = dict()

	for palabra in s_General: #Recorre todas las palabras de la colección(sección body).
		contArticulos = 0
		Ni = 0
		for documento in l_Documentos:   #recorre la lista de articulos
			if palabra in documento[2]: # Solo identifica si la palabra esta en el documento, no cuantas veces aparece en cada documento.
				Ni += 1				   # Aumenta el ni (numero de documentos) en el que aparece la palabra
		if Ni >= minNi: 
			d_Palabras[palabra] = Ni   #Se agregan a una lista, para despues ordenarla de mayor a menor.		
	l_Palabras = sorted(d_Palabras.items(),key=operator.itemgetter(1), reverse = True)    #Se ordena la lista con respecto a cantidad de "ni" de cada palabra.
	# print(listaPalabras)
	diccionarioPalabras = dict()
	cantidadDePalabras = 0
	with open("dicc.txt","w",encoding="UTF-8") as archivoDiccs: #Se genera el archivo de texto "dics.txt"
		for palabra in l_Palabras:
			# palabraFiltrada = re.sub("[^a-z\\d+.\\/]","",palabra[0]) ESTO YA SE HIZO
			# if palabraFiltrada not in stop_words:	ESTO YA SE VERIFICO
			archivoDiccs.write(palabra[0] + "\t" + str(palabra[1]) + "\n") 
			cantidadDePalabras += 1 #SE LLEVA UN CONTEO DE CUANTAS PALABRAS; PARA AL FINAL FACILITAR EL CÁLCULO DE LAS FÓRMULAS (línea del
											#for conteoPalabras in range(len(infoGI[conteoPalabras][1])): 192 aprox )
	final = default_timer()
	print( "Tardó ", final-inicio, " segundos en generar 'dicc.txt'.")
	return d_TablasGI, d_Palabras
		#TXT DE PRUEBA; PARA VISUALIZAR LAS PALABRAS Y SUS CALCULOS RESPECTIVOS:**************************************************************************
		#*******************************************************************************************************************************+

def generarConjuntoPalabrasAndDatosParaGI(l_Documentos,d_Clases):  #Genera un diccionario para toda la colección.
	conjuntoPalabras = set()
	tablasCalculoGI = dict()       #Esta lista contiene toda la informacion para el calculo de ganancia de información, cada indice es una palabra.

	for documento in l_Documentos:
		texto = documento[2]	#Se hace una lista de los terminos en el texto del articulo
		# print("ID",documento[1])
		# print("TEXTO:",texto)
		for termino in texto:
			if termino not in conjuntoPalabras:
				conjuntoPalabras.add(termino)
				palabra, clases = generarTablaGI(termino,l_Documentos,d_Clases)
				tablasCalculoGI[palabra] = clases

	#LA FUNCIÓN "generarDiccionariosGeneralAndDatosGI", RETORNA EL DICCIONARIO GENERAL PARA EL CÁLCULO
	#DEL "dicc.txt" Y UNA LISTA CON TODAS LAS PALABRAS Y SUS DATOS PARA PROCEDER CON
	#EL CÁLCULO DE GANACIA DE INFORMACIÓN. (SIMPLEMENTE SERÍA RECORRER LA LISTA DE PALABRAS
	# Y SU RESPECTIVO DICCIONARIO DE CLASES Y VALORES).
	return conjuntoPalabras,tablasCalculoGI

def generarTablaGI(palabra, l_Documentos, d_Clases):

	#EL DICCIONARIO DE CLASES POR PALABRA LLEVA EL SIGUIENTE ORDEN 
	#-> {clase: [termi-i , -termi-i, total], ... clase: [termi-i , -termi-i, total]}   
	d_ClasesPorPalabra = dict()  

	for documento in l_Documentos:
		clase = documento[0] #El indice 0 es la clase (topic) del articulo
		texto = documento[2] #El indice 2 es el body del artículo, la lista de palabras del body.
		if palabra in texto: 
			if clase in d_ClasesPorPalabra:
				d_ClasesPorPalabra[clase][0] += 1
				d_ClasesPorPalabra[clase][1] -= 1
			else:
				total = d_Clases[clase]
				d_ClasesPorPalabra[clase] = [1, total - 1, total]
	# print(palabra.upper())
	# for llave, valor in d_ClasesPorPalabra.items():
	# 	print(llave,valor)
	return palabra, d_ClasesPorPalabra

def generarGananciaDeInformacion(d_TablasGI, d_Palabras, N):
	inicio = default_timer()
	l_Calculos_Ec_PorClase = [] 
	sumatoria_Ec = 0
	primeraSumatoria = segundaSumatoria = 0

	with open("infoGanaciaInformacion.txt","w",encoding="UTF-8") as archivoInfoGI: 
		for palabra, clases in d_TablasGI.items(): #Recorre las tablas de valores para GI de las palabras.
			archivoInfoGI.write("Palabra: " + palabra + "\n")    #PALABRA.

			for clase, datos in clases.items():   #Recorre las clases de cada palabra.
				n_ik = datos[0]
				_n_ik = datos[1]
				nc_k = datos[2]

				archivoInfoGI.write("\t\tClase:" + str(clase) + "\n\t\t\t")
				#escribe -> (clase , itermi-i , -itermi-i , totalDeClase)
				archivoInfoGI.write(str("Info de la clase:") + "\n" + "\t\t\t\t\t" + 
									str(n_ik) + "\t\t" + 
									str(_n_ik) + "\t\t" + 
									str(nc_k)+ "\n")

				#SE CALCULA LA FORMULA E(C)
				probabilidad = nc_k / N # nck/N
				Ec_Individual = probabilidad * (math.log2(probabilidad)) * -1  #Aquí se calcula el E(C) de cada clase
				sumatoria_Ec += Ec_Individual   #Al mismo tiempo se va realizando la sumatoria.
				l_Calculos_Ec_PorClase.append(Ec_Individual)   #Se ingresan los E(C) individualmente a una lista en caso de necesitarse más adelante. REVISAR.


				#SE CALCULA UNA PARTE DE LA FORMULA E(C,iterm_i)
				# termi_no_i = infoGI[contPalabras][1][contClasesPorPalabra][1]   #La cantidad de clases en las que no estuvo
				# termi_i = infoGI[contPalabras][1][contClasesPorPalabra][0]
				#La primera y segunda sumatoria de E(C,〖term〗_i ) se calculará aquí para ahorrar iteraciones. 
				if n_ik == 0:
					n_ik = 0.000001
					# print("para que no se indefiniera el logaritmo se le sumó '0.000001' a termi_i (" + str(f"{infoGI[contPalabras][0]}") 
					# + ") La palabra es ->  " + f"{palabraActual}" )

				if _n_ik == 0:
					_n_ik = 0.0000000000000000000000000001
					# print("para que no se indefiniera el logaritmo se le sumó '0.000001' a termi_no_i (" + str(f"{infoGI[contPalabras][1]}") 
					# + ") La palabra es ->  " + f"{palabraActual}" )

				primeraSumatoria += n_ik * math.log2(n_ik) #* - 1
				segundaSumatoria += _n_ik * math.log2(_n_ik) #* -1
				

				#el ni se obtiene llamando al diccionario -> listaDePalabras

	#SE TERMINA DE CALCULAR LA FÓRMULA E(C,iterm_i).
	d_EC_Termi = dict()  #DICCIONARIO PARA METER LAS PALABRAS Y SU RESPECTIVO VALOR DE FÓRMULA:
	for palabra in d_Palabras:
		#print(conteoPalabras, cantidadDePalabras)
		#print(infoGI[conteoPalabras][0])
		ni = d_Palabras[palabra]
		EC_term_i = (ni * math.log2(ni) + (N - ni) * math.log2(N - ni) - primeraSumatoria - segundaSumatoria)/N
		d_EC_Termi[palabra] = EC_term_i
		# print(diccionario_E_C_Termi)

	d_EC_Termi = sorted(d_EC_Termi.items(), key=operator.itemgetter(1), reverse = True)
	with open("GICalculada.txt","w",encoding="UTF-8") as archivoGI: 
		for termino in d_EC_Termi:
			archivoGI.write(termino[0] + "\t\t" + str(termino[1]) + "\n")
	# print(listaDeCalculos_Ec_PorClase[0])
	# print(sumatoria_Ec)
	final = default_timer()
	print( "Tardó ", final-inicio, " segundos en generar 'infoGanaciaInformacion.txt'.")
















