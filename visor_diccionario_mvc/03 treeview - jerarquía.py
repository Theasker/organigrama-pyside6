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
        self.resize(800, 500)

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
        self.info.setText("Ejercicio 3: filas con hijos (estructura en árbol).")

        # Nodo padre
        deptos = QStandardItem("Departamentos")
        deptos_val = QStandardItem("") # Vacío porque es contenedor
        self.model.appendRow([deptos, deptos_val])

        # Hijo 1 del nodo padre
        tec = QStandardItem("Tecnología")
        tec_val = QStandardItem("") # Contenedor
        deptos.appendRow([tec, tec_val])

        # Nietos (hijos de Hijo 1)
        tec.appendRow([QStandardItem("responsable"), QStandardItem("Mauricio Segura")])
        tec.appendRow([QStandardItem("equipo"), QStandardItem("3 personas")])

        # Hijo 2 del nodo padre
        compras = QStandardItem("Compras")
        compras_val = QStandardItem("") # Contenedor
        deptos.appendRow([compras, compras_val])
        compras.appendRow([QStandardItem("responsable"), QStandardItem("Ana López")])

        # Expander todo el árbol
        self.treeview.expandAll()     

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow("QStandardItemModel - Intro")
    window.show()
    sys.exit(app.exec())