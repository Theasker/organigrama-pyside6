import settings
import json

from reportlab.platypus import Paragraph, SimpleDocTemplate, Image, Table, TableStyle, HRFlowable, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm

class Dict2pdf:
    def __init__(self, data, niveles_a_mostrar=3, filename="organigrama.pdf", info_nivel="Todos"):
        self.data = data
        self.niveles_a_mostrar = niveles_a_mostrar
        self.info_nivel = info_nivel
        
        self.doc = SimpleDocTemplate(
            filename, 
            pagesize=landscape(A4),
            title="Organigrama del Gobierno de Aragón",
            author="Mauricio Segura Ariño"
        )

        # Establecer márgenes
        self.doc.leftMargin = 10
        self.doc.rightMargin = 10
        self.doc.topMargin = 10
        self.doc.bottomMargin = 10

        self.styles = getSampleStyleSheet()
        self.estilos_niveles = {}

        self.story = []
        self._cabecera_doc(self.story)

        self.agregar_organo_a_pdf(self.data, self.story, niveles_a_mostrar=self.niveles_a_mostrar)
        self.doc.build(self.story, onFirstPage=self._pie_pagina, onLaterPages=self._pie_pagina)
    
    def _cabecera_doc(self, story):
        # --- 1. Imágen ---
        #image_path = "assets/GobiernodeAragon-1-Positivo-RGB-color.png"
        image_path = settings.LOGO_PATH
        img = Image(image_path)
        aspect_ratio = img.imageWidth / img.imageHeight
        # tamaño de un máximo de 30mm de la imagen
        max_width = 80 * mm
        max_height = max_width / aspect_ratio
        img.drawHeight = max_height
        img.drawWidth = max_width
        
        # --- 2. Columna derecha: Título y subtítulo ---
        columna_derecha = []
        titulo = "<h1>ORGANIGRAMA: GOBIERNO DE ARAGÓN</h1>"
        columna_derecha.append(Paragraph(titulo, self.styles['Heading1']))
        subtitulo = f"Niveles mostrados: {self.info_nivel}"        
        columna_derecha.append(Paragraph(subtitulo, self.styles['Heading2']))

        # --- 3. Tabla que recibe LISTA de FILAS. Cada FILA es una LISTA de CELDAS
        datos_tabla = [[img, columna_derecha]]

        # Calculamos los anchos para que ocupe todo el papel
        ancho_col_img = 80 * mm + 10 * mm
        ancho_col_derecha = self.doc.width - ancho_col_img - 10 * mm
        ancho_tabla = [ancho_col_img, ancho_col_derecha]

        tabla_header = Table(datos_tabla, colWidths=ancho_tabla)
        
        # --- 4. Estilos de la tabla ---
        estilo_tabla = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), # Todas las celdas centradas verticalmente
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'), # Todas las celdas alineadas a la izquierda
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey), # Rejilla en toda la tabla

            ('BOTTOMPADDING', (0,0), (-1, -1), 5), # Espaciado inferior
            ('TOPPADDING', (0,0), (-1, -1), 5), # Espaciado superior
            ('BACKGROUND', (1, 0), (1, 0), colors.lightgrey),
        ])
        tabla_header.setStyle(estilo_tabla)

        tabla_header.spaceAfter = 3 * mm # Espacio después de la tabla
        
        # --- 5. Añadir a la story ---
        story.append(tabla_header)

        # Línea separadora
        linea = HRFlowable( width="100%", thickness=0, color=colors.black, spaceAfter=5, spaceBefore=5)
        story.append(linea)
    
    def agregar_organo_a_pdf(self, datos, story, nivel=0, niveles_a_mostrar=99):
        # 1. extraer datos del diccionario actual
        codigo = datos.get("codigo", "")
        nombre = datos.get("nombre", "")
        hijos = datos.get("hijos", [])

        # 2. Creamos texto
        texto = f"<b>{codigo}</b> - {nombre}"
        
        # 3. Estilo dinámico
        if self.estilos_niveles.get(nivel) is None:
            # creo nuevo elemento del diccionario de estilos con el nuevo estilo
            self.estilos_niveles[nivel] = self._obtener_estilo(nivel)
        estilo_nodo = self.estilos_niveles[nivel]

        # 4. Añadir el párrafo
        story.append(Paragraph(texto, estilo_nodo))
        
        # 5. Recorrer todos los hijos incrementando el nivel
        if nivel < niveles_a_mostrar:
            for hijo in hijos:
                self.agregar_organo_a_pdf(hijo, story, nivel + 1, niveles_a_mostrar)
                if nivel == 0:
                    story.append(Spacer(1, 5*mm))

    def _obtener_estilo(self, nivel):
        # Dame una escala de colores en degradado según el nivel
        if nivel == 0:
            color = colors.darkorange
            size = 13
        elif nivel == 1:
            color = colors.darkblue
            size = 12
        elif nivel == 2:
            color = colors.darkgreen
            size = 11
        else:
            color = colors.black
            size = 10

        estilo_nodo = ParagraphStyle(
            name=f"EstiloNivel{nivel}",
            parent=self.styles['Normal'],
            leftIndent=nivel * 25,
            spaceBefore=3,
            textColor=color,
            fontSize=size
        )
        return estilo_nodo

    def _pie_pagina(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        # Dibujar el número de página en la coordenada (x,y)
        canvas.drawString(self.doc.width - 50, 15, f"Página {doc.page}")
        canvas.restoreState()

if __name__ == "__main__":
    from siu2dict_openpyxl import SIU_to_dict, URL
    siu = SIU_to_dict(URL)
    
    if siu.arbol_completo:
        print(json.dumps(siu.arbol_completo, ensure_ascii=False, indent=4))
        pdf = Dict2pdf(siu.arbol_completo)
    else:
        datos_raw = siu.procesar_excel_ligero()
        if datos_raw:
            siu.arbol_completo = siu.crear_arbol(datos_raw)
            # parámetros: diccionario de organismos, niveles a mostrar
            pdf = Dict2pdf(siu.arbol_completo, 2)
        else:
            print("No se pudo crear el árbol porque no se cargó el Excel.")