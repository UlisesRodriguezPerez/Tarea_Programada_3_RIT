from extraerAtributos import *
from funcionesAuxiliares import *

def seleccionar_terminos(archivo, numMejores, minNc, minNt, prefijo):

	# Variables globales
	Datos =  Body = Topics = Tags = []
	Datos = [Body, Topics, Tags]
	leerColeccion(archivo,minNc)

	# print (Datos)
	
seleccionar_terminos("reut2-001.sgm",0,100,0,0)
