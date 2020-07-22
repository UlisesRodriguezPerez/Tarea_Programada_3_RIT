from extraerAtributos import *
from funcionesAuxiliares import *

def seleccionar_terminos(archivo, numMejores, minNc, minNt, prefijo):
	inicio = default_timer()
	# Variables globales
	Datos =  Body = Topics = Tags = []
	Datos = [Body, Topics, Tags]
	leerColeccion(archivo,minNc)

	final = default_timer()
	print( "\n En total el programa tardó ", final-inicio)
	# print (Datos)
	
seleccionar_terminos("reut2-001.sgm",0,1,0,0)
