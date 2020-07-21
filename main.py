from extraerAtributos import *
from funcionesAuxiliares import *

def seleccionar_terminos(archivo, numMejores, minNc, minNt, prefijo):

	# Variables globales
	Datos =  Body = Topics = Tags = []
	Datos = [Body, Topics, Tags]
	leerColeccion(archivo)

	print (Datos)
	
seleccionar_terminos("reut2-001.sgm",123,123,123,13)
