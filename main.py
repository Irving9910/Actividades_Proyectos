import os
import io
import time
import re

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
                        if char.isalpha() or char.isspace():
                            newFile.write(char)
                    elif char == ">":
                        putIt = True

            oneFileTimeEnd = time.perf_counter()
            log.write(os.path.join(filesPath, filename) + f"  {oneFileTimeEnd - oneFileTimeStart:0.4f} segundos" + "\n")
        newFile.close()
    f.close()

diccionario = dict()
lastPath = None
# Ordener las palabras alfabeticamente y contar las repetidas
for filename in os.listdir(noHTMLPath):
    diccionarioAuxiliar = dict()
    with open(os.path.join(noHTMLPath, filename), 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            line = line.lower()
            words = line.split(" ")

            for word in words:
                if word in diccionario:
                    #Añadir una repeticion
                    diccionario[word][0] = diccionario[word][0] + 1

                    #Si la palabra no está en el diccionario auxiliar, significa que estamos en otro documento y por lo tanto se necesita agregar +1 al campo de documentos
                    if not word in diccionarioAuxiliar:
                        diccionario[word][1] = diccionario[word][1] + 1

                    #Agregar la palabra al diccionario auxiliar para que no vuelva a entrar al punto anterior si es el mismo documento
                    if lastPath != filename:
                        diccionarioAuxiliar[word] = True
                else:
                    #La palabra no existe en el diccionario, por lo tanto agregarla
                    diccionario[word] = [1, 1]
    lastPath = filename
    
#Escribir en un nuevo documento todas las palabras, su numero de repeticiones y en cuantos documentos se repitieron:
with io.open(tokenized + "tokenized.txt", 'w', encoding="utf-8") as newFile:
    for key in sorted(diccionario.keys()):
        # palabra ; #repeticiones ; #documentos
        wordListed = key + " ; " + str(diccionario[key][0]) + " ; " + str(diccionario[key][1]);
        newFile.write(wordListed + "\n")

# Termina cronometro de apertura de files
filesTimeEnd = time.perf_counter()

log.write(f"\nTiempo total de abrir archivos {filesTimeEnd - filesTimeStart:0.4f} segundos\n")

exeTimeEnd = time.perf_counter()
log.write(f"\nTiempo total de ejecución {exeTimeEnd - exeTimeStart:0.4f} segundos\n")
