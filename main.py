import os
import io
import time
import re
from collections import Counter

exeTimeStart = time.perf_counter()
# Matricula de alumno
matricula = "2728638"
# Ruta donde se tienen los archivos
# filesPath = "D:\\Mis documentos\\TecMilenio\\8vo Semestre\\Proyectos\\CS13309_Archivos_HTML\\Files"
# logPath = "D:\\Mis documentos\\TecMilenio\\8vo Semestre\\Proyectos\\CS13309_Archivos_HTML"

# MIKE'S PATH
filesPath = "C:\\Users\\pez-1\\Downloads\\CS13309_Archivos_HTML\\Files\\";
logPath = "C:\\Users\\pez-1\\Downloads\\CS13309_Archivos_HTML";
noHTMLPath = "C:\\Users\\pez-1\\Downloads\\CS13309_Archivos_HTML\\noHTML\\";
#alphaOrder = "C:\\Users\\pez-1\\Downloads\\CS13309_Archivos_HTML\\alphaOrder\\";
tokenized = "C:\\Users\\pez-1\\Downloads\\CS13309_Archivos_HTML\\tokenized\\"
stoplistFile = "C:\\Users\\pez-1\\Downloads\\CS13309_Archivos_HTML\\StopList.txt"

# Borra log.txt
if os.path.exists(os.path.join(logPath, "a1_" + matricula + ".txt")):
    os.remove(os.path.join(logPath, "a1_" + matricula + ".txt"))

# Comienza cronometro de apertura de files
filesTimeStart = time.perf_counter()

# Crear el log de tiempo
log = open(os.path.join(logPath, "a1_" + matricula + ".txt"), "a")

# Itera para obtener los nombres de los archivos dentro de la carpeta Files
for filename in os.listdir(filesPath):

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
            log.write(os.path.join(filesPath, filename) + f"  {oneFileTimeEnd - oneFileTimeStart:0.4f} segundos" + "\n")
        newFile.close()
    f.close()

stopList = []

#Archivo de STOPLIST
with open(stoplistFile, 'r', encoding='utf-8', errors='ignore') as stopListFile:
    for line in stopListFile:
        line = line.strip("\n")
        stopList.append(line)

diccionario = dict()
diccionario = []

diccionarioGeneral = dict()
diccionarioGeneral = []
lastPath = None

# Ordener las palabras alfabeticamente y contar las repetidas
for filename in os.listdir(noHTMLPath):
    diccionario = []
    with open(os.path.join(noHTMLPath, filename), 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            line = line.lower()
            words = line.split(" ")

            for word in words:
                if not word in stopList and len(word)>1:
                    word.lstrip()
                    match = any(item.get('path', "NONE") == filename and item.get('palabra', "NONE PALABRA") == word for item in diccionario)

                    if match:
                        matchPalabra = next(l for l in diccionario if l['path'] == filename and l["palabra"] == word)
                        matchPalabra["repeticiones"] = matchPalabra["repeticiones"] + 1

                    else:
                        diccionario.append({"path": filename, "repeticiones": 1, "palabra": word})
    diccionarioGeneral.extend(diccionario)
    lastPath = filename

#Ordenar alfabeticamente
diccionarioGeneral = sorted(diccionarioGeneral, key = lambda i: (i['palabra']))

#Quitar las palabras que tengan menos de 10 repeticiones
diccionarioGeneral = [d for d in diccionarioGeneral if d['repeticiones'] > 10]

#Escribir el archivo de posting
with io.open(tokenized + "posting.txt", 'w', encoding="utf-8") as newFile:
    indice = 1
    for index in range(len(diccionarioGeneral)):
        if not len(diccionarioGeneral[index].get('palabra')) == 0:
            #Linea por si queremos checar que letra es
            #newFile.write(str(indice)+". "+diccionarioGeneral[index].get('palabra')+" || "+str(diccionarioGeneral[index].get('path')) + " || " + str(diccionarioGeneral[index].get('repeticiones')) + "\n")
            newFile.write(str(indice)+". " + str(diccionarioGeneral[index].get('path')) + " || " + str(diccionarioGeneral[index].get('repeticiones')) + "\n")
            indice += 1

#Escribir el diccionario
with io.open(tokenized + "diccionario.txt", 'w', encoding="utf-8") as newFile:
    indice = 1
    signs = Counter(k['palabra'] for k in sorted(diccionarioGeneral, key = lambda i: (i['palabra'])) if k.get('palabra'))
    for (palabra, documentos) in sorted(signs.most_common()):
            newFile.write(palabra+" || "+str(documentos)+" || "+ str(indice) +"\n")
            indice += documentos

# Termina cronometro de apertura de files
filesTimeEnd = time.perf_counter()

log.write(f"\nTiempo total de abrir archivos {filesTimeEnd - filesTimeStart:0.4f} segundos\n")

exeTimeEnd = time.perf_counter()
log.write(f"\nTiempo total de ejecución {exeTimeEnd - exeTimeStart:0.4f} segundos\n")
