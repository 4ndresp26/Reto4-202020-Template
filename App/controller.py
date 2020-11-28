"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
from App import model
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos

def loadTrips(citibike):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(citibike, filename)
    return citibike

def loadFile(citibike, tripfile):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(citibike, trip)
    return citibike
# ___________________________________________________

# ___________________________________________________
#  Funciones para consultas
def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def numSCC(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.numSCC(analyzer)


def sameCC(sc,station1, station2):
    """
    Numero de componentes fuertemente conectados
    """
    return model.sameCC(sc,station1, station2)
    

def hasPath(analyzer, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    return model.hasPath(analyzer, destStation)

def servedRoutes(analyzer):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    maxvert, maxdeg = model.servedRoutes(analyzer)
    return maxvert, maxdeg

def Rutas_edad(analyzer,opt):
    if opt == "1":
        menor=0
        mayor=10
    elif opt == "2":
        menor=11
        mayor=20
    elif opt == "3":
        menor=21
        mayor=30
    elif opt == "4":
        menor=31
        mayor=40
    elif opt == "5":
        menor=41
        mayor=50
    elif opt == "6":
        menor=51
        mayor=60
    elif opt == "7":
        menor=61
        mayor=200
    else:
        return("opción no valida")
    cond='año_lleg'
    condt='año_sal'
    ruta=None
    inicial,num=model.Rutas_edad(analyzer,menor,mayor,cond)
    final,number=model.Rutas_edad(analyzer,menor,mayor,condt)
    model.minimumCostPaths(analyzer,inicial)
    if hasPath(analyzer, final) != False:
        ruta=model.minimumCostPath(analyzer,final)
        lista=[]
        for i in ruta:
            for llave in ruta[i]:
                if ruta[i][llave] != None:
                    x=(ruta[i]["info"]['vertexA'],ruta[i]["info"]['vertexB'])
                    lista.append(x)
                else:
                    ruta=lista
                    Rt={"e_i":inicial,"e_f":final,"n":num,"num":number,"ruta":ruta}
                    return Rt
        

        
def Mas_cercana(analyzer, ubi1, ubi2):
    inicial=model.Estacion_cercana(analyzer, ubi1)
    final=model.Estacion_cercana(analyzer, ubi2)
    return inicial,final



def top_llegada(analyzer):
    lista=model.top_llegada(analyzer)
    cond="nombre"
    for i in lista:
        print ("      *",lector_id(analyzer, i,cond))



def min_use(analyzer):
    lista=model.min_use(analyzer)
    Top=[None,None,None]
    Min=[100,100,100]
    for i in lista:
        for valor in range(0,len(Min)):
            if lista[i] < Min[valor] and i not in Top:
                Min[valor]=lista[i]
                Top[valor]=i
    cond="nombre"
    for i in Top:
        print ("      *",lector_id(analyzer, i,cond))



def top_salida(analyzer):
    lista=model.top_salida(analyzer)
    cond="nombre"
    for i in lista:
        print ("      *",lector_id(analyzer, i, cond))
    


def lector_id(analyzer, ids, caract):
    return (analyzer["stops"][ids][caract])



def mant_bikes(analyzer,id,fecha):
    INFO={"Estaciones":[],"libre":0,"uso":0}
    rt=model.mant_bikes(analyzer,id,fecha)
    time=model.temp_use(analyzer,id,fecha)
    if rt["Estaciones"]!=[]:
        for id in rt["Estaciones"]:
            INFO["Estaciones"].append(lector_id(analyzer,id,"nombre"))
    INFO["libre"]=time-rt["duracion"]
    INFO["uso"]=rt["duracion"]
    return INFO
    
# ___________________________________________________