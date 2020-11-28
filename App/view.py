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


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

initialStation = None
recursionLimit = 20000
# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de citibike")
    print("3- Calcular componentes conectados")
    print("4- Ruta turística Circular: ")
    print("5- Ruta por edad: ")
    print("6- Estación más cercana: ")
    print("7- Mantenimiento de bicicletas(Bono): ")
    print("0- Salir")
    print("*******************************************")


def optionTwo():
    print("\nCargando información de citibike....")
    controller.loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))


def optionThree():
    print ( 'El número de componentes conectados es:'  +
          str ( controller.numSCC( cont )))
    print ( "la estación" , id1 , "y" , id2 , controller.sameCC( cont , id1 , id2 ))

def optionFour():
    print('Las estaciones Top de llegada son: ')
    controller.top_llegada(cont)
    print('Las estaciones  Top de Salida son: ')
    controller.top_salida(cont)
    print('Las estaciones menos usadas son: ')
    controller.min_use(cont)

def optionFive():
    rango=input("""Rangos de edad:
    1.0 años - 10 anños.
    2.11 años - 20 anños.
    3.21 años - 30 anños.
    4.31 años - 40 anños.
    5.41 años - 50 anños.
    6.51 años - 60 anños.
    7.60 años o más. 
    Ingrese un rango: """)
    dicc=controller.Rutas_edad(cont,rango)
    if dicc=="opción no valida":
        print (dicc)
    else:
        print("La estación con mas salidas en ese rango fue ",controller.lector_id(cont,dicc["e_i"],"nombre"),", con ",dicc["n"])
        print("La estación con mas llegadas en ese rango fue ",controller.lector_id(cont,dicc["e_f"],"nombre"),", con ",dicc["num"])
        if dicc["ruta"] == None:
            print("No estan conectadas esas estaciones")
        else:
            print("La mejor ruta para recorrer estas estaciones es: ")
            for dato in dicc["ruta"]:
                inicial,final=dato
                print("de: ", controller.lector_id(cont,inicial,"nombre"), " a ",controller.lector_id(cont,final,"nombre"))

def optionSix():
    local1=float(input("Digite  la ubicación de partida (latitud): "))
    local2=float(input("Digite  la ubicación de partida (longitud): "))
    ubi1=(local1,local2)
    local1=float(input("Digite  la ubicación de llegada (latitud): "))
    local2=float(input("Digite  la ubicación de llegada (longitud): "))
    ubi2=(local1,local2)
    lat,lon=controller.Mas_cercana(cont, ubi1, ubi2)
    name1=controller.lector_id(cont,lat,"nombre")
    name2=controller.lector_id(cont,lon,"nombre")
    print("La estación mas cercana al punto de partida es: ",name1,", id:", lat)
    print("La estación mas cercana al punto de llegada es: ",name2,", id:", lon)

def optionSeven():
    fecha=input("Digite la fecha de consulta: ")
    id=input("Digite la id de la bicicleta a consultar: ")
    info=controller.mant_bikes(cont,id,fecha)
    if info["Estaciones"]==[]:
        print("la bicicleta no tuvo recorridos hasta ese dia.")
    else:
        print("las estaciones por las que ha pasado la bicicleta son: ",info["Estaciones"])
        print("El tiempo en uso de la bicicleta fue de : ",info["uso"], " segundos")
        print("El tiempo en libre de la bicicleta fue de : ",info["libre"], " segundos")

def optionEight():
    maxvert, maxdeg = controller.servedRoutes(cont)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        id1 = input ( "digitie el id de la estación 1:" )
        id2 = input ( "digitie el id de la estación 2:" )
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)