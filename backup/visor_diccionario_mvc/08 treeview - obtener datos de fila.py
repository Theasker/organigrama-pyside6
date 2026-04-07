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
        self.info.setText("Ejercicio 8: selección. Muestra en la barra de estado la clave/valor seleccionados.")
        # Conectar la señal de selección a un método

        self.model.appendRow([QStandardItem("Monitores"), QStandardItem("42")])
        self.model.appendRow([QStandardItem("Teclados"), QStandardItem("15")])
        self.model.appendRow([QStandardItem("Ratones"), QStandardItem("27")])
        self.treeview.selectionModel().selectionChanged.connect(self.on_selection_changed)
    
    def on_selection_changed(self, selected, deselected):
        # Coge el primer índice seleccionado (si hay alguno)
        indexes = self.treeview.selectionModel().selectedIndexes()
        if not indexes:
            self.statusBar().clearMessage()
            return
        # Normalmente hay dos índices por fila (col 0 y col 1); nos quedamos con la fila
        idx = indexes[0] # Primer índice seleccionado
        row = idx.row() # Fila del índice
        clave = self.model.item(row, 0).text() # Clave (columna 0)
        valor = self.model.item(row, 1).text() # Valor (columna 1)
        self.statusBar().showMessage(f"Seleccionado=> Clave: {clave}, Valor: {valor}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow("QStandardItemModel - Intro")
    window.show()
    sys.exit(app.exec())