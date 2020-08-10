from extraerAtributos import *
from funcionesAuxiliares import *

# Nomenclatura
#L_ o l_ es para listas
#D_ o d_ es para diccionarios
#S_ o s_ es para sets o conjuntos

def seleccionar_terminos(archivo, numMejores, minNc, minNi, prefijo):
	inicio = default_timer()

	L_Documentos, D_Clases = leerColeccion(archivo)
	D_ClasesMinNC, N = generarClasesTxt(D_Clases, minNc,prefijo)
	L_DocumentosMinNC = generarDocsTxt(L_Documentos,D_ClasesMinNC,prefijo) 
	D_TablasGI, D_Palabras = generarDiccTxt(L_DocumentosMinNC, D_ClasesMinNC, minNi,prefijo)
	generarGananciaDeInformacion(D_TablasGI, D_Palabras,D_Clases,N,prefijo)

	final = default_timer()
	print( "\n En total el programa tardó ", final-inicio)

	# print (Datos)

#seleccionar_terminos(NOMBRE_ARCHIVO,NUM_MEJORES,MIN_NC,MIN_NI,PREFIJO)
seleccionar_terminos("TP3-Prueba.sgm",0,0,0,"pr2_")
