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
        self.info.setText("Ejercicio 5: roles de datos (UserRole). Guardamos un ID oculto por fila.")

        USER_ID_ROLE = Qt.UserRole + 1 # Definimos un rol personalizado

        def add_item(clave, valor, id_):
            item_k = QStandardItem(clave)
            item_v = QStandardItem(valor)
            # Guardamos el ID en ambos ítems usando el rol personalizado (misma fila)
            item_k.setData(id_, USER_ID_ROLE)
            item_v.setData(id_, USER_ID_ROLE)
            self.model.appendRow([item_k, item_v])
        
        # Agregamos filas con IDs ocultos
        add_item("n1_serie", "SN123456", id_=101)
        add_item("n2_serie", "SN789012", id_=102)
        add_item("n3_serie", "SN345678", id_=103)

        # Leer el ID oculto del primer ítem como demostración
        idex_val = self.model.index(0, 1) # Primera fila, segunda columna
        id_guardado = self.model.data(idex_val, USER_ID_ROLE)
        self.statusBar().showMessage(f"ID oculto del primer ítem: {id_guardado}") 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow("QStandardItemModel - Intro")
    window.show()
    sys.exit(app.exec())