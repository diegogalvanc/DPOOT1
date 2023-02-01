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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

Se define la estructura de un catálogo de libros.
El catálogo tendrá  una lista para los libros.

Los autores, los tags y los años se guardaran en
tablas de simbolos.
"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {"crimes": None,
                "dateIndex": None,
                "areaIndex": None,

                }

    analyzer["crimes"] = lt.newList("SINGLE_LINKED", compareIds)
    analyzer["dateIndex"] = om.newMap(omaptype="RBT",
                                      comparefunction=compareDates)
    # TODO lab 9, crear el indice ordenado por areas reportadas
    analyzer["areaIndex"] = om.newMap(omaptype="RBT",
                                      comparefunction=compareAreas)

    return analyzer


# Funciones para agregar informacion al catalogo


def addCrime(analyzer, crime):
    """
    adicionar un crimen a la lista de crimenes y en el arbol
    """
    lt.addLast(analyzer["crimes"], crime)
    updateDateIndex(analyzer["dateIndex"], crime)
    # TODO lab 9, actualizar el indice por areas reportadas
    updateAreaIndex(analyzer["areaIndex"], crime)
    return analyzer


def updateAreaIndex(map, crime):
    """
    actualiza el indice de areas reportadas con un nuevo crimen
    si el area ya existe en el indice, se adiciona el crimen a la lista
    si el area es nueva, se crea una entrada para el indice y se adiciona
    y si el area son ["", " ", None] se utiliza el valor por defecto 9999
    """
    # TODO lab 9, implementar actualizacion del indice por areas reportadas

    occurredarea = crime["REPORTING_AREA"]
    entry = om.get(map, occurredarea)

    # revisar si el area es un str vacio ["", " ", None]
    if occurredarea == ["", " ", None]:
       areaentry = me.getValue(entry)
       # area desconocida es 9999
       om.put(map, occurredarea, "9999")

    # revisar si el area ya esta en el indice
    elif entry is None:
        areaentry = newDataEntry(crime)
        # area desconocida es 9999
        om.put(map, occurredarea, areaentry)

    # si el area ya esta en el indice, adicionar el crimen a la lista
    else:
        areaentry = me.getValue(entry)
    addDateIndex(areaentry, crime)

    return map


def newAreaEntry(crime):
    """
    Crea una entrada para el indice de areas reportadas
    """
    # TODO lab 9, crear una entrada para el indice de areas reportadas
    entry = {"areaIndex": None, "lstcrimes": None}
    entry["areaIndex"] = m.newMap(numelements=30,
                                     maptype="PROBING",
                                     comparefunction=compareAreas)
    entry["lstcrimes"] = lt.newList("SINGLE_LINKED", compareDates)
    lt.addLast(entry["lstcrimes"], crime)

    return entry


def addAreaIndex(areaentry, crime):
    """
    Adiciona un crimen a la lista de crimenes de un area
    """
    # TODO lab 9, adicionar crimen a la lista de crimenes de un area
    lst = areaentry["lstcrimes"]
    lt.addLast(lst, crime)
    areaIndex = areaentry["areaIndex"]
    areaentry = m.get(areaIndex, crime["REPORTING_AREA"])
    if (areaentry is None):
        entry = newAreaEntry(crime["REPORTING_AREA"])
        lt.addLast(entry["lstareas"], crime)
        m.put(areaIndex, crime["REPORTING_AREA"], entry)
    else:
        entry = me.getValue(areaentry)
        lt.addLast(entry["lstareas"], crime)

    return areaentry



def updateDateIndex(map, crime):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = crime["OCCURRED_ON_DATE"]
    crimedate = datetime.datetime.strptime(occurreddate, "%Y-%m-%d %H:%M:%S")
    entry = om.get(map, crimedate.date())
    if entry is None:
        datentry = newDataEntry(crime)
        om.put(map, crimedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, crime)
    return map


def addDateIndex(datentry, crime):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry["lstcrimes"]
    lt.addLast(lst, crime)
    offenseIndex = datentry["offenseIndex"]
    offentry = m.get(offenseIndex, crime["OFFENSE_CODE_GROUP"])
    if (offentry is None):
        entry = newOffenseEntry(crime["OFFENSE_CODE_GROUP"], crime)
        lt.addLast(entry["lstoffenses"], crime)
        m.put(offenseIndex, crime["OFFENSE_CODE_GROUP"], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry["lstoffenses"], crime)
    return datentry


def newDataEntry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {"offenseIndex": None, "lstcrimes": None}
    entry["offenseIndex"] = m.newMap(numelements=30,
                                     maptype="PROBING",
                                     comparefunction=compareOffenses)
    entry["lstcrimes"] = lt.newList("SINGLE_LINKED", compareDates)
    lt.addLast(entry["lstcrimes"], crime)
    return entry


def newOffenseEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {"offense": None, "lstoffenses": None}
    ofentry["offense"] = offensegrp
    ofentry["lstoffenses"] = lt.newList("SINGLE_LINKED", compareOffenses)
    lt.addLast(ofentry["lstoffenses"], crime)
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def crimesSize(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer["crimes"])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer["dateIndex"])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer["dateIndex"])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer["dateIndex"])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer["dateIndex"])


def indexHeightAreas(analyzer):
    """
    Altura del arbol por areas
    """
    # TODO lab 9, leer la altura del arbol por areas
    return om.height(analyzer["areaIndex"])


def indexSizeAreas(analyzer):
    """
    Numero de elementos en el indice por areas
    """
    # TODO lab 9, leer el numero de elementos en el indice por areas
    return om.size(analyzer["areaIndex"])


def minKeyAreas(analyzer):
    """
    Llave mas pequena por areas
    """
    # TODO lab 9, leer la llave mas pequena por areas
    return om.minKey(analyzer["areaIndex"])


def maxKeyAreas(analyzer):
    """
    Llave mas grande por areas
    """
    # TODO lab 9, leer la llave mas grande por areas
    return om.maxKey(analyzer["areaIndex"])


def getCrimesByRangeArea(analyzer, initialArea, FinalArea):
    """
    Retorna el numero de crimenes en un rango de areas
    """
    # TODO lab 9, completar la consulta de crimenes por rango de areas
    lst = om.values(analyzer["areaIndex"], initialArea, FinalArea)
    totalcrimes = 0
    for lstarea in lt.iterator(lst):
        totalcrimes += lt.size(lstarea["lstcrimes"])
    return totalcrimes


def getCrimesByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer["dateIndex"], initialDate, finalDate)
    totalcrimes = 0
    for lstdate in lt.iterator(lst):
        totalcrimes += lt.size(lstdate["lstcrimes"])
    return totalcrimes


def getCrimesByRangeCode(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    crimedate = om.get(analyzer["dateIndex"], initialDate)
    if crimedate["key"] is not None:
        offensemap = me.getValue(crimedate)["offenseIndex"]
        numoffenses = m.get(offensemap, offensecode)
        if numoffenses is not None:
            return m.size(me.getValue(numoffenses)["lstoffenses"])
    return 0


# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareAreas(area1, area2):
    """
    Compara dos areas
    """
    # area = "REPORTING_AREA"
    if (area1 == area2):
        return 0
    elif (area1 > area2):
        return 1
    else:
        return -1


def compareOffenses(offense1, offense2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1
