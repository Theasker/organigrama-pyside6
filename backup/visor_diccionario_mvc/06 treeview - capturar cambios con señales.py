from hmac import new
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
        self.resize(420, 500)

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
        self.treeview.header().setDefaultSectionSize(200)  # Tamaño por defecto
        
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
        self.info.setText("Ejercicio 6: señales. Detectamos cambios de texto en los valores.")

        # Poblamos 2 filas editables en columna 1 (valor)
        def add_item( clave, valor):
            row = [QStandardItem(clave),QStandardItem(valor)]
            row[0].setEditable(False) # Hacer no editable la columna 0 (clave)
            row[1].setEditable(True)  # Hacer editable la columna 1 (valor)
            self.model.appendRow(row)
            self.model.itemChanged.connect(self.on_item_changed)
        
        # Items de ejemplo
        add_item("monitores", "42")
        add_item("teclados", "17")

    def on_item_changed(self, item: QStandardItem):        
        # Sólo nos interesan cambios en la columna 1 (valor)
        if item.column() == 0:
            return
        row = item.row() # Fila del ítem cambiado
        key = self.model.item(row, 0).text()   # Clave
        new_value = item.text()          # Nuevo valor
        self.statusBar().showMessage(f"Cambio en '{key}': nuevo valor = {new_value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow("QStandardItemModel - Intro")
    window.show()
    sys.exit(app.exec())