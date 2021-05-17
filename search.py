import os
import io
import time
import re
from collections import Counter
import sys

palabraBuscar = str(sys.argv[1]).lower()
inputPath = str(sys.argv[2])
outputPath = str(sys.argv[3])

# Matricula de alumno
matricula = "2728638"
# Ruta donde se tienen los archivos
# Files Path Irving
# filesPath = "D:\\Mis documentos\\TecMilenio\\8vo Semestre\\Proyectos\\CS13309_Archivos_HTML\\Files"
# Tokenized Irving
# tokenized = "D:\\Mis documentos\\TecMilenio\\8vo Semestre\\Proyectos\\CS13309_Archivos_HTML\\tokenized\\"
# logPath = "D:\\Mis documentos\\TecMilenio\\8vo Semestre\\Proyectos\\CS13309_Archivos_HTML"

# Path to CS13309_Archivos_HTML
htmlPath = "C:\\Users\\pez-1\\Downloads\\CS13309_Archivos_HTML\\"

# MIKE'S PATH
filesPath = htmlPath + inputPath
logPath = htmlPath
noHTMLPath = htmlPath + "noHTML\\"
#alphaOrder = "C:\\Users\\pez-1\\Downloads\\CS13309_Archivos_HTML\\alphaOrder\\";
tokenized = htmlPath + outputPath + "\\"
stoplistFile = htmlPath + "StopList.txt"

# Borra log.txt
if os.path.exists(os.path.join(logPath, "a1_" + matricula + ".txt")):
    os.remove(os.path.join(logPath, "a1_" + matricula + ".txt"))

# Comienza cronometro de apertura de files

# Crear el log de tiempo
log = open(os.path.join(logPath, "a1_" + matricula + ".txt"), "a")

#Obtener los nombres de los archivos
diccionarioDocumentos = dict()
indexName = 1

# Itera para obtener los nombres de los archivos dentro de la carpeta Files
for filename in os.listdir(filesPath):
    diccionarioDocumentos[filename] = indexName
    indexName += 1

    # Abre los archivos concatenando la varianble filesPath + el nombre del file en iteración
    oneFileTimeStart = time.perf_counter()
    with open(os.path.join(filesPath, filename), 'r', encoding='utf-8', errors='ignore') as f:



        # Crear nuevo archivo
        with io.open(noHTMLPath + filename, 'w', encoding="utf-8") as newFile:
            putIt = None
            # Leer linea por linea
            for line in f:
                newLine = re.sub("\s\s+", " ", line)
                for char in newLine:
                    if char == "<":
                        putIt = False
                    elif (char != '<') and (putIt == True):
                        if char.isalpha() or char.isspace() and char != "\t":
                            newFile.write(char)
                    elif char == ">":
                        putIt = True

            oneFileTimeEnd = time.perf_counter()
        newFile.close()
    f.close()

stopList = []

diccionario = dict()
diccionario = []

diccionarioGeneral = dict()
diccionarioGeneral = []
lastPath = None

listaPalabras = []


# Ordener las palabras alfabeticamente y contar las repetidas
print("Ordenando palabras y contando repetidas")
for filename in os.listdir(noHTMLPath):
    diccionario = []
    with open(os.path.join(noHTMLPath, filename), 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            line = line.lower()
            words = line.split(" ")

            for word in words:
                if len(word)>1:
                    word.lstrip()
                    match = any(item.get('path', "NONE") == filename and item.get('palabra', "NONE PALABRA") == word for item in diccionario)

                    if match:
                        matchPalabra = next(l for l in diccionario if l['path'] == filename and l["palabra"] == word)
                        matchPalabra["repeticiones"] = matchPalabra["repeticiones"] + 1

                    else:
                        diccionario.append({"path": filename, "repeticiones": 1, "palabra": word})

        for index in range(len(diccionario)):
            if diccionario[index].get('palabra') == str(palabraBuscar):
                listaPalabras.append(diccionario[index].get('path'))
                break

    diccionarioGeneral.extend(diccionario)
    lastPath = filename


def retrievefunc():
    exeTimeStart = time.perf_counter()
    index = 1
    print("Ejecutando Retrieve Document" )
    # Escribir el archivo de posting
    with io.open(tokenized + "retrieve.txt", 'w', encoding="utf-8") as newFile:
        newFile.write("Archivos con la palabra: " + palabraBuscar + "\n")

        for documento in listaPalabras:
            newFile.write(str(index) + ".     " + documento + "\n")
            index += 1

    exeTimeEnd = time.perf_counter()
    log.write(f"\nTiempo total de ejecución {exeTimeEnd - exeTimeStart:0.4f} segundos\n")

retrievefunc()