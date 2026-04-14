from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor # <--- Corregido: H mayúscula

class DictToPDF:
    def __init__(self, datos_arbol):
        self.datos = datos_arbol
        self.width, self.height = landscape(A4)
        self.margin = 20 * mm
        self.line_height = 8 * mm
        self.indent_size = 10 * mm 
        self.pag_number = 1
        
    def exportar(self, file_path):
        c = canvas.Canvas(file_path, pagesize=landscape(A4))
        self.y_pos = self.height - self.margin
        self._preparar_pagina(c)
        self._dibujar_nodo(c, self.datos, self.margin, nivel=0)
        c.save()

    def _preparar_pagina(self, c):
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(HexColor("#2c3e50")) # <--- Corregido
        c.drawString(self.margin, self.height - 15 * mm, "ORGANIGRAMA: GOBIERNO DE ARAGÓN")
        
        c.setStrokeColor(HexColor("#ff9800")) # <--- Corregido
        c.setLineWidth(1)
        c.line(self.margin, self.height - 18 * mm, self.width - self.margin, self.height - 18 * mm)
        
        self._draw_footer(c)
        self.y_pos = self.height - 25 * mm

    def _dibujar_nodo(self, c, nodo, x, nivel):
        if self.y_pos < 25 * mm:
            c.showPage()
            self.pag_number += 1
            self._preparar_pagina(c)

        if nivel == 0:
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(HexColor("#d35400")) # <--- Corregido
        elif nivel == 1:
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(HexColor("#2c3e50")) # <--- Corregido
        else:
            c.setFont("Helvetica", 9)
            c.setFillColor(HexColor("#333333")) # <--- Corregido

        codigo = nodo.get('codigo', '---')
        nombre = nodo.get('nombre', 'Sin nombre')
        
        c.drawString(x, self.y_pos, codigo)
        c.drawString(x + 30 * mm, self.y_pos, nombre[:130])

        if nivel > 0:
            c.setStrokeColor(HexColor("#bdc3c7")) # <--- Corregido
            c.setLineWidth(0.2)
            c.line(x - 3*mm, self.y_pos + 3*mm, x - 3*mm, self.y_pos)
            c.line(x - 3*mm, self.y_pos + 1*mm, x - 1*mm, self.y_pos + 1*mm)

        self.y_pos -= self.line_height

        hijos = nodo.get('hijos', [])
        if hijos:
            for hijo in hijos:
                self._dibujar_nodo(c, hijo, x + self.indent_size, nivel + 1)

    def _draw_footer(self, c):
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(HexColor("#7f8c8d")) # <--- Corregido
        c.drawString(self.margin, 10 * mm, "Fuente: SIU Aragón")
        texto_pag = f"Página {self.pag_number}"
        c.drawCentredString(self.width / 2, 10 * mm, texto_pag)
        c.drawRightString(self.width - self.margin, 10 * mm, "Copia oficial")

if __name__ == "__main__":
    from siu2dict_openpyxl import SIU_to_dict
    URL = "https://aplicaciones.aragon.es/siu_admin/download_descargar"
    siu = SIU_to_dict(URL)
    if siu.existe_local():
        print("Archivo local encontrado, procesando..." )
        if siu.arbol_completo:
            # mostramos el árbol completo en consola
            print(json.dumps(siu.arbol_completo, ensure_ascii=False, indent=4))
        else:
            # realizamos el proceso completo para obtener el árbol
            datos_raw = siu.procesar_excel_ligero()
            if datos_raw:
                siu.arbol_completo = siu.crear_arbol(datos_raw)
                pdf = DictToPDF(siu.arbol_completo)
    else:
        print("Archivo local no encontrado, descargando..." )