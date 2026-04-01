import requests
import os
import zipfile
import pandas as pd
import glob
import warnings

def descargar_zip(url):
    try:
        # Realizamos la petición GET a la URL
        data = requests.get(url, timeout=60)
        
        # Verificamos si la descarga fue exitosa (Código 200)
        # Si hubo un error (ej. 404 Not Found), esto lanzará una excepción.
        data.raise_for_status()

        # Guardamos el archivo de manera local
        # Verificamos que existe el directorio de destino
        DIR_TARGET = r".\tmp"
        os.makedirs(DIR_TARGET, exist_ok=True)
        # Creamos el fichero local para guardar la respuesta
        local_file = 'local_copy.zip'
        final_zip_file = os.path.join(DIR_TARGET, local_file)
        with open(final_zip_file, 'wb')as file:
            file.write(data.content)
        descomprimir_zip(final_zip_file)
        procesar_excel(DIR_TARGET)
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error: {e}")    

def descomprimir_zip(fichero_zip=r".\tmp\local_copy.zip"):
    try:
        DIR_TARGET = r".\tmp"
        # Verifico que existe el directorio
        os.makedirs(DIR_TARGET, exist_ok=True)
        # abro el zip en modo lectura
        with zipfile.ZipFile(fichero_zip, 'r') as zip_ref:
            # extraigo todos los archivos
            zip_ref.extractall(DIR_TARGET)
        print("Zip descomprimido correctamente")
    except FileNotFoundError:
        print(f"El archivo {fichero_zip} no fue encontrado")
    except PermissionError:
        print(f"Permiso denegado: Cierra el archivo Excel en '{DIR_TARGET}' antes de continuar.")
    except zipfile.BadZipFile:
        print(f"El archivo {fichero_zip} no es un archivo zip válido")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def procesar_excel(directorio=r"backup\tmp"):
    try:
        # Buscamos cualquier archivo .xlsx en el directorio
        patron = os.path.join(directorio, "*.xlsx")
        archivos = glob.glob(patron)
        # Filtramos archivos temporales de Excel (que empiezan por ~$)
        archivos = [f for f in archivos if not os.path.basename(f).startswith("~$")]
        print(f"Archivos encontrados: {archivos}")
        if archivos:
            archivo_excel = archivos[0] # Tomamos el primero que encontremos
            print(f"Procesando: {archivo_excel}")
            
            
            
            
            # with warnings.catch_warnings():
            #     warnings.filterwarnings("ignore", category=UserWarning, message="Workbook contains no default style")
            #     df = pd.read_excel(archivo_excel)
            crear_arbol(df)
        else:
            print("No se encontró ningún archivo .xlsx en el directorio.")
    except Exception as e:
        print(f"Error al procesar el Excel: {e}")

def crear_arbol(df):
    print("#"*100)

    # 1. Crear diccionario auxiliar: código → nombre del organismo
    nombres = {}
    # creo el primer nodo raiz padre de todos
    nombres['ORG00001'] = "GOBIERNO DE ARAGÓN (RAÍZ)"
    
    for _, row in df.iterrows():
        codigo = str(row['CÓDIGO ORGANISMO']).strip()
        nombre = str(row['ORGANISMO']).strip()
        nombres[codigo] = nombre
    # 1. FIN BLOQUE _________________________

    # 2. Crear el diccionario children: padre → lista de hijos
    """
    Devuelve el nombre del organismo a partir de su código.
    Si no existe, devuelve el propio código.
    """
    def obtener_nombre(codigo): 
        return nombres.get(codigo, codigo)

    children = {}
    for _, row in df.iterrows():
        padre = str(row['CÓDIGO ORGANISMO PADRE']).strip()
        hijo = str(row['CÓDIGO ORGANISMO']).strip()

        # Si el padre aún no existe en el diccionario -> crear su lista
        if padre not in children:
            children[padre] = []

        # Agregar el hijo a la lista del padre
        children[padre].append(hijo)
    
    # Ordenación del diccionario children ------------------
    """
    Devuelve el nombre del organismo a partir de su código.
    Si no existe, devuelve el propio código.
    """
    def obtener_nombre(codigo): 
        return nombres.get(codigo, codigo)
    for padre in children:
        lista_hijos = children[padre]
        # Ordena la lista de hijos según el nombre del organismo
        lista_hijos.sort(key=obtener_nombre)
    # FIN Ordenación del diccionario ---------------------

    # 3. Función recursiva que construye los nodos uno a uno
    def construir_nodo(codigo):
        nodo = {
            'codigo': codigo,
            'nombre': nombres.get(codigo, codigo),
            'hijos': []
        }
        if codigo in children:
            # Recorrer todos los hijos
            for hijo in children[codigo]:
                nodo_hijo = construir_nodo(hijo)
                nodo['hijos'].append(nodo_hijo)
        return nodo

    # # 4. Contruir arbol completo desde la raíz ORG00001
    arbol_completo = construir_nodo('ORG00001')
    print(arbol_completo)
    exportar_arbol_json(arbol_completo)
    return arbol_completo
      
def exportar_arbol_json(arbol, ruta="arbol_organismos.json", con_bom=False):
    import json
    enc = "utf-8-sig" if con_bom else "utf-8"
    with open(ruta, 'w', encoding=enc) as f:
        json.dump(arbol, f, ensure_ascii=False, indent=4, sort_keys=True)
    print(f"✅ JSON exportado en UTF-8{' (con BOM)' if con_bom else ''}: {ruta}")



URL = "https://aplicaciones.aragon.es/siu_admin/download_descargar"
# descargar_zip(URL)
# descomprimir_zip()
procesar_excel()