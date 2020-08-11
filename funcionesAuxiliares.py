# coding=<UTF-8>

import io 
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
	stopwords.append(" ")
	return stopwords

def eliminarStopWords(texto, stopwords):# Funcion para eliminar stopWords
	textoSinStopWords = ""  
	palabrasDelTexto = texto.split()

	# Se quitan los stop words
	for palabra in palabrasDelTexto:
		palabra = palabra.replace("\n","")
		palabra = palabra.replace("\t","")
		if palabra != '' and not palabra in stopwords:
			textoSinStopWords += palabra + " "
	return textoSinStopWords

def dejarPuntosSoloEnNumeros(texto): 
	# texto = re.sub(r"[^a-z0-9,.\"\'']"," ",texto)
	# 		#PENDINETE -> Averiguar si es más rápido usar una expresión regular para todas a la vez.
	# texto = texto.replace(",", "")		
	# texto = texto.replace("\'","")
	# texto = texto.replace("\"","")
	
	nuevoTexto = re.sub("(?<!\\d)\\.(?=\\d)|(?<=\\d)\\.(?!\\d)|(?<!\\d)\\.(?!\\d)","", texto)   #Expresión regular que elimina los puntos menos entre números.
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

def generarClasesTxt(Clases, minNc, prefijo): #Esta funcion genera el txt de clases y llama a la funcion para generar el txt de Docs. Deben de ser complementarias.
	inicio = default_timer()
	#topicsAceptados = []             #El diccionario de topics aceptados es para saber cuales si son aceptados por minNc
	ClasesOrdenadas = sorted(Clases.items(), key=operator.itemgetter(1), reverse = True)	#Es una lista, no un diccionario
	ClasesMinNC = dict() #Este diccionario será usado para calcular la diferencia de cada termino, restando el total de apariciones de esa 
									  #clase - la cantidad de clases en las que apareció la palabra.
	totalDeClases = 0
	with open(prefijo+"clases.txt","w",encoding="UTF-8") as archivoClases:
		for clase in ClasesOrdenadas:
			totalDeClases += clase[1]
			archivoClases.write(str(clase[0]) + "\t" + str(clase[1]) + "\n")
			ClasesMinNC[clase[0]] = clase[1]    #Diccionario con las clases que se piden por parámetro.
			if clase[1] < minNc:
				break

	final = default_timer()
	print( "Tardó ", final-inicio, " segundos en generar 'clases.txt'.")
	return ClasesMinNC, totalDeClases
		

def generarDocsTxt(l_Documentos, d_Clases, prefijo):
	inicio = default_timer()
	l_DocumentosPermitidos = []
	with open(prefijo+"docs.txt","w",encoding="UTF-8") as archivoDocs:
		for articulo in l_Documentos:
			if articulo[0] in d_Clases.keys(): #Si el articulo se encuentra en la lista de llaves del dict de clases aceptadas, significa que también está en las clases restringidas.
				archivoDocs.write(str(articulo[1]) + "\t" + articulo[0] + "\n")   #El formato es (ID, Clase a la que pertenece)
				l_DocumentosPermitidos.append(articulo)
	final = default_timer()
	print( "Tardó ", final-inicio, " segundos en generar 'docs.txt'.")
	return l_DocumentosPermitidos


def generarDiccTxt(l_Documentos,d_Clases,minNi,prefijo):
	inicio = default_timer()
	#listaDeDiccionarios = generarListaDeDiccionarios(listaDeArticulosPermitidos)  #Se llama la función "generarListaDeDiccionarios" para nada más proceder a la comparación.
	s_General, d_TablasGI = generarConjuntoPalabrasAndDatosParaGI(l_Documentos,d_Clases) 
	d_Palabras = dict()

	for palabra in s_General: #Recorre todas las palabras de la colección(sección body).
		contArticulos = 0
		Ni = 0
		palabra = str(palabra)
		for documento in l_Documentos:   #recorre la lista de articulos
			if palabra in documento[2]: # Solo identifica si la palabra esta en el documento, no cuantas veces aparece en cada documento.
				Ni += 1				   # Aumenta el ni (numero de documentos) en el que aparece la palabra
		if Ni >= minNi: 
			
			d_Palabras[palabra] = Ni   #Se agregan a una lista, para despues ordenarla de mayor a menor.		
	l_Palabras = sorted(d_Palabras.items(),key=operator.itemgetter(1), reverse = True)    #Se ordena la lista con respecto a cantidad de "ni" de cada palabra.
	# print(listaPalabras)
	diccionarioPalabras = dict()
	cantidadDePalabras = 0
	with open(prefijo+"dicc.txt","w",encoding="UTF-8") as archivoDiccs: #Se genera el archivo de texto "dics.txt"
		for palabra in l_Palabras:

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
	tablasCalculoGI = dict()    #Esta lista contiene toda la informacion para el calculo de ganancia de información, cada indice es una palabra.
	
	for documento in l_Documentos:
		texto = documento[2]	#Se hace una lista de los terminos en el texto del articulo
		for termino in texto:		
			if termino not in conjuntoPalabras:		
				conjuntoPalabras.add(termino)
				clases = generarTablaGI(termino,l_Documentos,d_Clases)
				tablasCalculoGI[termino] = clases

	#LA FUNCIÓN "generarDiccionariosGeneralAndDatosGI", RETORNA EL DICCIONARIO GENERAL PARA EL CÁLCULO
	#DEL "dicc.txt" Y UNA LISTA CON TODAS LAS PALABRAS Y SUS DATOS PARA PROCEDER CON
	#EL CÁLCULO DE GANACIA DE INFORMACIÓN. (SIMPLEMENTE SERÍA RECORRER LA LISTA DE PALABRAS
	# Y SU RESPECTIVO DICCIONARIO DE CLASES Y VALORES).
	return conjuntoPalabras,tablasCalculoGI

def generarTablaGI(palabra, l_Documentos, d_Clases):

	#EL DICCIONARIO DE CLASES POR PALABRA LLEVA EL SIGUIENTE ORDEN 
	#-> {clase: [termi-i , -termi-i, total], ... clase: [termi-i , -termi-i, total]}   
	d_ClasesPorPalabra = dict()  	#PENDIENTE -> Cambiar el dict por una lista normal, para más rápidez.
	# Se inicializa el diccionario de clases para el termino
	for clase in d_Clases:
		d_ClasesPorPalabra[clase] = [0,d_Clases[clase],d_Clases[clase]]

	for documento in l_Documentos:
		clase = documento[0] #El indice 0 es la clase (topic) del articulo
		if palabra in documento[2]: 	#Documento[2] es la lista de palabras del body
			if clase in d_ClasesPorPalabra:
				d_ClasesPorPalabra[clase][0] += 1
				d_ClasesPorPalabra[clase][1] -= 1

	return d_ClasesPorPalabra

def generarGananciaDeInformacion(d_TablasGI, d_Palabras, d_Clases, N, prefijo,num_Mejores):
	inicio = default_timer()
	sumatoria_Ec = 0
	primeraSumatoria = segundaSumatoria = 0
	d_Ec = dict()
	d_GI = dict()
	d_GI_TXT = dict()
	giTXT = ""
	contadorNumMejores = 0

	#SE CALCULA LA FORMULA E(C)
	for clase in d_Clases:
		nc_k = d_Clases[clase]
		if nc_k == 0:
			Ec = 0
		else:
			probabilidad = nc_k / N # nck/N
			Ec = -probabilidad * (math.log2(probabilidad))  #Aquí se calcula el E(C) de cada clase
		sumatoria_Ec += Ec   #Al mismo tiempo se va realizando la sumatoria.
		giTXT += ("\nE("+clase+"= " + str(Ec))
	giTXT += ("\nE(Clases)= "+str(sumatoria_Ec)+"\n")

	for palabra, clases in d_TablasGI.items(): #Recorre las tablas de valores para GI de las palabras.
		if palabra in d_Palabras:
			giTXT = ""
			giTXT += ("\nPalabra: " + palabra)
			# Se resetean para cada palabra
			primeraSumatoria = segundaSumatoria = Ec_term_i = GI_term_i = sum_Ec_term_i = sum_GI_term_i = 0;
			for clase, datos in clases.items():   #Recorre las clases de cada palabra.
				n_ik = datos[0]
				_n_ik = datos[1]
				nc_k = datos[2]

				# giTXT += ("\t\tClase:" + str(clase) + "\n\t\t\t")
				# giTXT += (str("Info de la clase:") + "\n" + "\t\t\t\t\t" + 
				# 					str(n_ik) + "\t\t" + 
				# 					str(_n_ik) + "\t\t" + 
				# 					str(nc_k)+ "\n")

				#SE CALCULA UNA PARTE DE LA FORMULA E(C,iterm_i)
				if n_ik == 0:
					n_ik = 1

				if _n_ik == 0:
					_n_ik = 1

				primeraSumatoria += n_ik * math.log2(n_ik)
				segundaSumatoria += _n_ik * math.log2(_n_ik)
				
			#SE TERMINA DE CALCULAR LA FÓRMULA E(C,iterm_i).
			
			ni = d_Palabras[palabra]
			if (ni == N): #Caso en el que una palabra aparece en todos los documentos
				ni = N-0.000000000000001
			EC_term_i = (ni * math.log2(ni) + (N - ni) * math.log2(N - ni) - primeraSumatoria - segundaSumatoria)/N
			giTXT += ("\tE(Clases),"+palabra+")= "+str(EC_term_i))
			GI_term_i = sumatoria_Ec - EC_term_i
			d_GI[palabra] = GI_term_i
			d_Ec[palabra] = EC_term_i
			giTXT += ("\tGI("+palabra+")= "+str(GI_term_i)+"\n")
			
			d_GI_TXT[palabra] = giTXT

	d_GI_TXT = sorted(d_GI_TXT.items(), key=operator.itemgetter(0))
	with open(prefijo+"gi.txt","w",encoding="UTF-8") as archivoInfoGI: 
		for texto in d_GI_TXT:
			#if contadorNumMejores < num_Mejores:
			archivoInfoGI.write(texto[1])
			#else:
			#	break
			contadorNumMejores += 1
	contadorNumMejores = 0
	d_GI = sorted(d_GI.items(), key=operator.itemgetter(1), reverse = True)
	with open(prefijo+"mejores.txt","w",encoding="UTF-8") as archivoGI: 
		archivoGI.write("termino \tEntropia\tGanancia de informacion\n")
		for termino in d_GI:
			if contadorNumMejores < num_Mejores:
				archivoGI.write(termino[0] + "\t\t" + str(d_Ec[termino[0]]) + "\t" +str(termino[1]) +"\n")
			else:
				break
			contadorNumMejores += 1
	final = default_timer()
	print( "Tardó ", final-inicio, " segundos en generar 'infoGanaciaInformacion.txt'.")
