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
import config
import datetime
from math import radians, cos, sin, asin, sqrt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
def newAnalyzer():
    citibike= {
                'stops': None,
                'connections': None,
                'components': None,
                'paths': None,
                'bikes': None
                    }
    citibike['stops'] = {}
    citibike['bikes'] = {}
    citibike["connections"] = gr.newGraph(datastructure='ADJ_LIST',
                                  directed=True,
                                  size=1000,
                                  comparefunction=compareStopIds)
    return citibike

# -----------------------------------------------------

# Funciones para agregar informacion al grafo

def addTrip(citibike, trip):
    """
    """
    origin = trip['start station id']
    destination = trip['end station id']
    if origin != destination:
        duration = int(trip['tripduration'])
        nombre=trip['start station name']
        apodo=trip['end station name']
        car=trip['birth year']
        u=(float(trip['start station latitude']),float(trip['start station longitude']))
        u2=(float(trip['end station latitude']),float(trip['end station longitude']))
        addStation(citibike, origin)
        addStation(citibike, destination)
        addConnection(citibike, origin, destination, duration)
        add_bike(citibike, trip)
        info_vert(citibike,origin,nombre,"año_lleg",car,u)
        info_vert(citibike,destination,apodo,"año_sal",car,u2)
    return citibike

def add_bike(citibike, trip):
    bike = trip['bikeid']
    Fecha_i=trip["starttime"]
    Fecha_f=trip["stoptime"]
    time=int(trip["tripduration"])
    est_vis=trip["start station id"]
    est_vis2=trip["end station id"]
    if bike not in citibike["bikes"]:
        citibike["bikes"][bike]={}
        citibike["bikes"][bike][Fecha_f]={"duracion":time,"estaciones":[]}
        citibike["bikes"][bike][Fecha_f]["estaciones"].append(est_vis)
        citibike["bikes"][bike][Fecha_f]["estaciones"].append(est_vis2)
    else:
        citibike["bikes"][bike][Fecha_f]={"duracion":time,"estaciones":[]}
        if est_vis not in citibike["bikes"][bike][Fecha_f]["estaciones"]:
            citibike["bikes"][bike][Fecha_f]["estaciones"].append(est_vis)
        if est_vis2 not in citibike["bikes"][bike][Fecha_f]["estaciones"]:
            citibike["bikes"][bike][Fecha_f]["estaciones"].append(est_vis2)

def info_vert(citibike,id,n,cat,a,u):
    if id not in citibike["stops"]:
        citibike["stops"][id]={"nombre":n,"año_lleg":[],"año_sal":[],"ubicación":u}
        citibike["stops"][id][cat].append(a)
    else:
        citibike["stops"][id][cat].append(a)

def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike ["connections"], stationid):
            gr.insertVertex(citibike ["connections"], stationid)
    return citibike

def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citibike ["connections"], origin, destination)
    if edge is None:
        gr.addEdge(citibike["connections"], origin, destination, duration)
    return citibike

# ==============================
# Funciones de consulta

def numSCC(analyzer):
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])

def sameCC(analyzer,station1,station2):
    return scc.stronglyConnected(analyzer['components'],station1,station2)

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer

def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)

def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    
    return gr.numVertices(analyzer['connections'])

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def top_llegada(analyzer):
    Top=[None,None,None]
    Max=[0,0,0]
    for i in analyzer["connections"]["indegree"]["table"]["elements"]:
        if i["value"]!=None:
            for valor in range(0,len(Max)):
                if i["value"] > Max[valor] and i["key"] not in Top:
                    Max[valor]=i["value"]
                    Top[valor]=i["key"]
    return Top

def top_salida(analyzer):
    Top=[None,None,None]
    Max=[0,0,0]
    for i in analyzer["connections"]["vertices"]["table"]["elements"]:
        if i["value"]!=None:
            if i["value"]["size"]!=0:
                for valor in range(0,len(Max)):
                    if i["value"]["size"]>Max[valor] and i["key"] not in Top:
                        Max[valor]=i["value"]["size"]
                        Top[valor]=i["key"]
    return Top

def min_use(analyzer):
    lista={}
    for i in analyzer["connections"]["indegree"]["table"]["elements"]:
        if i["value"]!=None:
            if i["key"] not in lista:
                lista[i["key"]]=i["value"]
            else:
                lista[i["key"]]=lista[i["key"]]+i["value"]
    for i in analyzer["connections"]["vertices"]["table"]["elements"]:
        if i["value"]!=None:
            if i["value"]["size"]!=0:
                if i["key"] not in lista:
                    lista[i["key"]]=i["value"]["size"]
                else:
                    lista[i["key"]]=lista[i["key"]]+i["value"]["size"]
    return lista

def Rutas_edad(analyzer,men,may,cond):
    lista={}
    for id in analyzer["stops"]:
        for data in analyzer["stops"][id][cond]:
            if (2020-int(data))>=men and (2020-int(data))<=may:
                if id in lista:
                    lista[id]=lista[id]+1
                else:
                    lista[id]=1
    May=0
    final=None,None
    for data in lista:
        if lista[data]>May:
            May=lista[data]
            final=data,lista[data]
    return final

def Estacion_cercana(analyzer,ubi):
    cerc=10000
    for i in analyzer['stops']:
        distance= harvesine( ubi, analyzer['stops'][i]["ubicación"] )
        if cerc > distance:
            cerc=distance
            id= i
    return id

def harvesine( ubi, ubi2):
    lat1,lon1=ubi2
    lat2,lon2=ubi
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return (c * r)

def mant_bikes(analyzer,id,fecha):
    rt={"duracion":0,"Estaciones":[]}
    fecha = datetime.datetime.strptime(str(fecha), "%Y-%m-%d")
    fecha=fecha.date()
    for Fecha in analyzer["bikes"][id]:
        Date = datetime.datetime.strptime(str(Fecha), '%Y-%m-%d %H:%M:%S.%f')
        Date=Date.date()
        print(Date,fecha)
        if Date < fecha or Date == fecha:
            rt["duracion"]=rt["duracion"]+analyzer["bikes"][id][Fecha]["duracion"]
            for est in analyzer["bikes"][id][Fecha]["estaciones"]:
                if est not in rt["Estaciones"]:
                    rt["Estaciones"].append(est)
    return rt

def temp_use(analyzer,id,fecha):
    Min=datetime.datetime.strptime("2050-01-01 00:00:00.0000", '%Y-%m-%d %H:%M:%S.%f')
    fecha= datetime.datetime.strptime(str(fecha), "%Y-%m-%d")
    for Fecha in analyzer["bikes"][id]:
        Date = datetime.datetime.strptime(str(Fecha), '%Y-%m-%d %H:%M:%S.%f')
        Min=min_date(Min,Date)
    Min.date()
    tiempo=(fecha-Min).total_seconds()
    return abs(tiempo)


# ==============================
# Funciones Helper
# ==============================

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name


# ==============================
# Funciones de Comparacion
# ==============================
def min_date(Fecha,fecha):
    if Fecha < fecha:
        return Fecha
    else:
        return fecha

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1


# ==============================

# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================