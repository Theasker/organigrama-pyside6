import requests
import os
import zipfile
import pandas as pd
import warnings

class SIU_to_dict():
    def __init__(self, url):
        # self.descargar_zip(url)
        # self.descomprimir_zip()
        # self.procesar_excel("tmp")
        df = self.procesar_excel()
        self.arbol_completo = None
        if df is not None:
            self.arbol_completo = self.crear_arbol(df)
        else:
            print("No se pudo crear el árbol porque no se cargó el Excel.")

    def descargar_zip(self, url):
        try:
            # Realizamos la petición GET a la URL
            data = requests.get(url, timeout=60)
            
            # Verificamos si la descarga fue exitosa (Código 200)
            # Si hubo un error (ej. 404 Not Found), esto lanzará una excepción.
            data.raise_for_status()

            # Guardamos el archivo de manera local
            # Verificamos que existe el directorio de destino
            DIR_TARGET = r"tmp"
            os.makedirs(DIR_TARGET, exist_ok=True)
            # Creamos el fichero local para guardar la respuesta
            local_file = 'local_copy.zip'
            final_zip_file = os.path.join(DIR_TARGET, local_file)
            with open(final_zip_file, 'wb')as file:
                file.write(data.content)
        except requests.exceptions.RequestException as e:
            print(f"Ocurrió un error: {e}")

    def descomprimir_zip(self,fichero_zip=r".\tmp\local_copy.zip"):
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

    def procesar_excel(self,directorio=r"tmp"):
        try:            
            # Obtenemos todos los ficheros del directorio
            files = os.listdir(directorio)
            # Verificamos que hay un fichero xlsx
            for file in files:
                if file.endswith("xlsx"):
                    archivo_excel = os.path.join(directorio, file)
            if archivo_excel:
                # Corregimos el warning de la libreria openpyxls
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=UserWarning)
                    # Creamos el dataframe                    
                    df = pd.read_excel(archivo_excel)
                return df
            else:
                print("No se encontró ningún archivo .xlsx en el directorio.")
        except Exception as e:
            print(f"Error al procesar el Excel: {e}")

    def crear_arbol(self, df):
        # Creamos diccionario auxiliar: código => nombre organismo
        nombres = {}
        nombres['ORG00001'] = "GOBIERNO DE ARAGÓN (RAÍZ)"        
        for _, row in df.iterrows():
            codigo = str(row['CÓDIGO ORGANISMO']).strip()
            nombre = str(row['ORGANISMO']).strip()
            nombres[codigo] = nombre
        # 1. FIN BLOQUE _________________________

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
        return arbol_completo

    def __str__(self, data, ident):
        ident = ident

        def recursive(item, level=0):
            if isinstance(item, dict): # Si es un diccionario
                for key, value in item.items():
                    print(f"{' ' * ident * level}{key}:")
                    recursive(value, level + 1) # Llamada recursiva para el valor, aumentando el nivel de indentación
            elif isinstance(item, list): # Si es una lista
                for value in item:
                    recursive(value, level + 1)
            else: # Si es un valor simple
                print(f"{' ' * ident * level}{item}")
        
        recursive(data)
        return ""


if __name__ == "__main__":
    URL = "https://aplicaciones.aragon.es/siu_admin/download_descargar"
    siu = SIU_to_dict(URL)
    tree = siu.arbol_completo
    print(siu.__str__(tree, 2))
    
