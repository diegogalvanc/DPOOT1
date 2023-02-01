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
 """

import config as cf
from App import model
import datetime
import time
import csv

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
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, crimesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    crimesfile = cf.data_dir + crimesfile
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"),
                                delimiter=",")
    for crime in input_file:
        model.addCrime(analyzer, crime)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def crimesSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.crimesSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)


def indexHeightAreas(analyzer):
    """
    Altura del indice de areas (arbol)
    """
    # TODO lab 9, completar el llamado de indexHeightAreas()
    return model.indexHeightAreas(analyzer)


def indexSizeAreas(analyzer):
    """
    Numero de nodos en el arbol por areas
    """
    # TODO lab 9, completar el llamado de indexSizeAreas()
    return model.indexSizeAreas(analyzer)


def minKeyAreas(analyzer):
    """
    La menor llave del arbol por areas
    """
    # TODO lab 9, completar el llamado de minKeyAreas()
    return model.minKeyAreas(analyzer)


def maxKeyAreas(analyzer):
    """
    La mayor llave del arbol por areas
    """
    # TODO lab 9, completar el llamado de maxKeyAreas()
    return model.maxKeyAreas (analyzer)


def getCrimesByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, "%Y-%m-%d")
    finalDate = datetime.datetime.strptime(finalDate, "%Y-%m-%d")
    return model.getCrimesByRange(analyzer, initialDate.date(),
                                  finalDate.date())


def getCrimesByRangeCode(analyzer, initialDate,
                         offensecode):
    """
    Retorna el total de crimenes de un tipo especifico en una
    fecha determinada
    """
    initialDate = datetime.datetime.strptime(initialDate, "%Y-%m-%d")
    return model.getCrimesByRangeCode(analyzer, initialDate.date(),
                                      offensecode)


def getCrimesByRangeArea(analizer, initialArea, FinalArea):
    # TODO lab 9, completar el llamado para el req 5 para rangos de area
    """
    Retorna el total de crimenes en un rango de areas
    """
    # recuerde castear los parametros a int
    initialArea=int(initialArea)
    FinalArea=int(FinalArea)
    return model.getCrimesByRangeArea(analizer,initialArea,FinalArea)


# Funciones para medir tiempos de ejecucion


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
