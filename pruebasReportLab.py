import json

from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors

class dict2pdf:
    def __init__(self, data):
        self.doc = SimpleDocTemplate("guia_diccionarios.pdf", pagesize=landscape(A4))
        
        self.styles = getSampleStyleSheet()
        self.estilos_niveles = {}
        self.story = []
        self.data = data
        self.agregar_organo_a_pdf(self.data, self.story)
        self.doc.build(self.story)
        
    def agregar_organo_a_pdf(self, datos, story, nivel=0):
        # 1. extraer datos del diccionario actual
        codigo = datos["codigo"]
        nombre = datos["nombre"]
        hijos = datos["hijos"]

        # 2. Creamos texto
        texto = f"<b>{codigo}</b> - {nombre}"
        
        # 3. Estilo dinámico
        if self.estilos_niveles.get(nivel) is None:
            # creo nuevo elemento del diccionario de estilos con el nuevo estilo
            self.estilos_niveles[nivel] = self.obtener_estilo(nivel)
        estilo_nodo = self.estilos_niveles[nivel]

        # 4. Añadir el párrafo
        story.append(Paragraph(texto, estilo_nodo))

        # 5. Recorrer todos los hijos
        for hijo in hijos:
            self.agregar_organo_a_pdf(hijo, story, nivel + 1)

    def obtener_estilo(self, nivel):
        # Dame una escala de colores en degradado según el nivel
        if nivel == 0:
            color = colors.red
            size = 13
        elif nivel == 1:
            color = colors.blue
            size = 12
        elif nivel == 2:
            color = colors.green
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



if __name__ == "__main__":
    from datos import datos
    pdf = dict2pdf(datos)

