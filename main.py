import os
import time

exeTimeStart = time.perf_counter()
# Matricula de alumno
matricula = "2728638"
# Ruta donde se tienen los archivos
filesPath = "D:\\Mis documentos\\TecMilenio\\8vo Semestre\\Proyectos\\CS13309_Archivos_HTML\\Files"
logPath = "D:\\Mis documentos\\TecMilenio\\8vo Semestre\\Proyectos\\CS13309_Archivos_HTML"

# Borra log.txt
if os.path.exists(os.path.join(logPath, "a1_"+matricula+".txt")):
    os.remove(os.path.join(logPath, "a1_"+matricula+".txt"))

# Comienza cronometro de apertura de files
filesTimeStart = time.perf_counter()

# Crear el log de tiempo
log = open(os.path.join(logPath, "a1_"+matricula+".txt"), "a")

# Itera para obtener los nombres de los archivos dentro de la carpeta Files
for filename in os.listdir(filesPath):


# Abre los archivos concatenando la varianble filesPath + el nombre del file en iteración
    oneFileTimeStart = time.perf_counter()
    with open(os.path.join(filesPath, filename), 'r') as f:
        oneFileTimeEnd = time.perf_counter()
        log.write(os.path.join(filesPath, filename) + f"  {oneFileTimeEnd - oneFileTimeStart:0.4f} segundos" + "\n")


# Termina cronometro de apertura de files
filesTimeEnd = time.perf_counter()

log.write(f"\nTiempo total de abrir archivos {filesTimeEnd - filesTimeStart:0.4f} segundos\n")


exeTimeEnd = time.perf_counter()
log.write(f"\nTiempo total de ejecución {exeTimeEnd - exeTimeStart:0.4f} segundos\n")