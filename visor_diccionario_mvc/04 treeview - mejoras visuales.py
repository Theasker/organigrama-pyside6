import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTreeView, QLabel
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

class DemoWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(300, 500)

        self._create_widgets()
        self._create_layout()
        self.run_exercise()

    def _create_widgets(self):
        self.info = QLabel("Instrucciones irán apareciendo aquí.")
        self.info.setWordWrap(True) # Permitir salto de línea

        self.treeview = QTreeView(self) # Crear vista de árbol
        self.treeview.setAlternatingRowColors(True) # Colores alternos
        self.treeview.setUniformRowHeights(True)    # Mejor rendimiento
        self.treeview.header().setStretchLastSection(True) # Última columna estirada
        self.treeview.header().setDefaultSectionSize(300)  # Tamaño por defecto
        
        # Crear y configurar el modelo
        self.model = QStandardItemModel(self) # Crear modelo estándar
        self.model.setHorizontalHeaderLabels(["Clave", "Valor"]) # Encabezados
        self.treeview.setModel(self.model) # Conectar modelo a la vista

    def _create_layout(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        self.layout = QVBoxLayout(central_widget)
        self.layout.addWidget(self.info) # Agregar etiqueta al layout
        self.layout.addWidget(self.treeview) # Agregar vista al layout

        central_widget.setLayout(self.layout)

    def run_exercise(self):
        self.info.setText("Ejercicio 4: dición y formato (editable, alineación, fuente).")

        fila1 = [QStandardItem("monitores"), QStandardItem("42")]
        fila2 = [QStandardItem("portátiles"), QStandardItem("15")]

        # Hacemos que la olumna de valores sea editable y la clave no
        fila1[0].setEditable(False) # Clave no editable
        fila2[0].setEditable(True)  # Valores editable

        # Alineamos a la derecha la columna de valores
        fila1[1].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        fila2[1].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Estilo (opcional): ponemos la fuente en negrita para las claves
        fuente_negrita = fila1[0].font()
        fuente_negrita.setBold(True)
        fila1[0].setFont(fuente_negrita)

        self.model.appendRow(fila1)
        self.model.appendRow(fila2)  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow("QStandardItemModel - Intro")
    window.show()
    sys.exit(app.exec())