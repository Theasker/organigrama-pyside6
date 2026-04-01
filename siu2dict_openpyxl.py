import requests
import os
import zipfile
import openpyxl  # Mucho más ligero que Pandas
import json

class SIU_to_dict():
    def __init__(self, url):
        # Descomenta estas líneas si quieres que el proceso sea automático al instanciar
        # self.descargar_zip(url)
        # self.descomprimir_zip()
        
        datos_raw = self.procesar_excel_ligero()
        self.arbol_completo = None
        
        if datos_raw:
            self.arbol_completo = self.crear_arbol(datos_raw)
        else:
            print("No se pudo crear el árbol porque no se cargó el Excel.")

    def descargar_zip(self, url):
        try:
            data = requests.get(url, timeout=60)
            data.raise_for_status()
            
            dir_target = "tmp"
            os.makedirs(dir_target, exist_ok=True)
            
            final_zip_file = os.path.join(dir_target, 'local_copy.zip')
            with open(final_zip_file, 'wb') as file:
                file.write(data.content)
        except requests.exceptions.RequestException as e:
            print(f"Error en la descarga: {e}")

    def descomprimir_zip(self, fichero_zip=r"tmp/local_copy.zip"):
        try:
            dir_target = "tmp"
            os.makedirs(dir_target, exist_ok=True)
            with zipfile.ZipFile(fichero_zip, 'r') as zip_ref:
                zip_ref.extractall(dir_target)
            print("Zip descomprimido correctamente")
        except Exception as e:
            print(f"Error al descomprimir: {e}")

    def procesar_excel_ligero(self, directorio="tmp"):
        try:
            archivo_excel = None
            for file in os.listdir(directorio):
                if file.endswith(".xlsx"):
                    archivo_excel = os.path.join(directorio, file)
                    break
            
            if not archivo_excel:
                print("Error: No se encontró el archivo .xlsx en 'tmp'")
                return None

            # Cargamos el libro. Quitamos read_only para asegurar compatibilidad total con el buscador
            wb = openpyxl.load_workbook(archivo_excel, data_only=True)
            sheet = wb.active # El archivo de Aragón suele tener los datos en la primera hoja
            
            datos = []
            headers_found = False
            idx_codigo = idx_nombre = idx_padre = None

            for row in sheet.iter_rows(values_only=True):
                # 1. Ignorar filas vacías por completo
                if not any(row):
                    continue

                # 2. Si aún no tenemos cabeceras, buscamos la fila que las contiene
                if not headers_found:
                    # Normalizamos la fila para buscar las columnas
                    row_clean = [str(c).strip().upper() if c else "" for c in row]
                    if 'CÓDIGO ORGANISMO' in row_clean:
                        idx_codigo = row_clean.index('CÓDIGO ORGANISMO')
                        idx_nombre = row_clean.index('ORGANISMO')
                        idx_padre = row_clean.index('CÓDIGO ORGANISMO PADRE')
                        headers_found = True
                        continue # Saltamos a la siguiente fila (la primera de datos)
                
                # 3. Si ya encontramos las cabeceras, extraemos la información
                if headers_found:
                    # Validamos que la fila tenga el código del organismo (columna principal)
                    codigo_val = row[idx_codigo]
                    if codigo_val:
                        datos.append({
                            'codigo': str(codigo_val).strip(),
                            'nombre': str(row[idx_nombre]).strip() if row[idx_nombre] else "Sin nombre",
                            'padre': str(row[idx_padre]).strip() if row[idx_padre] else None
                        })

            wb.close()

            if not datos:
                print("Error: Se leyó el archivo pero no se extrajeron datos. Revisa los nombres de las columnas.")
                return None

            print(f"Éxito: {len(datos)} registros extraídos correctamente.")
            return datos
            
        except Exception as e:
            print(f"Error crítico procesando Excel: {e}")
            return None

    def crear_arbol(self, datos):
        nombres = {'ORG00001': "GOBIERNO DE ARAGÓN (RAÍZ)"}
        children = {}

        # Mapear nombres y relaciones en una sola pasada
        for item in datos:
            codigo = item['codigo']
            padre = item['padre']
            nombres[codigo] = item['nombre']
            
            if padre not in children:
                children[padre] = []
            children[padre].append(codigo)

        # Ordenar hijos por nombre para que el QTreeView luzca profesional
        for padre in children:
            children[padre].sort(key=lambda c: nombres.get(c, c))

        def construir_nodo(codigo):
            return {
                'codigo': codigo,
                'nombre': nombres.get(codigo, codigo),
                'hijos': [construir_nodo(h) for h in children.get(codigo, [])]
            }

        return construir_nodo('ORG00001')

    def dict2json(self, data, filename='arbol_completo.json'):
        if not data: return
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    URL = "https://aplicaciones.aragon.es/siu_admin/download_descargar"
    siu = SIU_to_dict(URL)
    if siu.arbol_completo:
        siu.dict2json(siu.arbol_completo)
        print("Proceso completado exitosamente.")