"""Ejemplo de uso de siu2dict.py

Este script muestra cómo ejecutar el flujo completo y obtener el diccionario de organización.

Requisitos:
- Instalar dependencias: pandas, requests, openpyxl.
- Tener el ZIP descargable o el XLSX en tmp/.
"""

from siu2dict import SIU_to_dict

# 1) Descarga y descompresión (si corresponde URL + ZIP)
#    El constructor actual de SIU_to_dict no usa la variable URL para esos pasos,
#    así que podemos invocarlos explícitamente.
URL = "https://aplicaciones.aragon.es/siu_admin/download_descargar"

siu = SIU_to_dict(URL)  # intentará procesar tmp/*.xlsx y crear el árbol

# Si ya tienes el archivo xlsx local en tmp/, puedes saltarte descargar/descomprimir
# siu = SIU_to_dict("dummy")

# 2) También puedes controlar manualmente el flujo (recomendado para claridad):
# siu.descargar_zip(URL)
# siu.descomprimir_zip(r"tmp/local_copy.zip")
# df = siu.procesar_excel("tmp")
# arbol = siu.crear_arbol(df)

# 3) Resultado final
arbol = siu.arbol_completo
print("Árbol completo (estructura de diccionario):")
print(arbol)

# 4) Ejemplo: navegar y mostrar un valor
if arbol:
    print("Nodo raíz:", arbol['nombre'], arbol['codigo'])
    if arbol['hijos']:
        print("Primer hijo:", arbol['hijos'][0]['nombre'], arbol['hijos'][0]['codigo'])
