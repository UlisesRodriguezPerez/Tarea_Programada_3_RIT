from extraerAtributos import *
from funcionesAuxiliares import *
from Constantes import *

def seleccionar_terminos(archivo, numMejores, minNc, minNi, prefijo):
	inicio = default_timer()
	# Variables globales
	Datos =  Body = Topics = Tags = []
	Datos = [Body, Topics, Tags]
	leerColeccion(archivo,minNc,minNi)

	final = default_timer()
	print( "\n En total el programa tardó ", final-inicio)
	# print (Datos)

seleccionar_terminos(NOMBRE_ARCHIVO,NUM_MEJORES,MIN_NC,MIN_NI,PREFIJO)
