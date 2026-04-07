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
        self.info.setText("Ejercicio 7: recorrer el modelo y sus hijos en consola.")

        # Creamos estructura con hijos
        padre = QStandardItem("Inventario") # Ítem padre
        padre_v = QStandardItem("")      # Valor vacío para padre
        self.model.appendRow([padre, padre_v]) # Agregar fila al modelo

        def _add_item(nombre, valor, padre=None):
            padre.appendRow([QStandardItem(nombre), QStandardItem(valor)])
        
        _add_item("Manzanas", "10 kg", padre)
        _add_item("Naranjas", "5 kg", padre)
        _add_item("Plátanos", "7 kg", padre)
        verduras = QStandardItem("Verduras")
        verduras_v = QStandardItem("")
        padre.appendRow([verduras, verduras_v])
        _add_item("Zanahorias", "3 kg", verduras)
        _add_item("Lechugas", "4 unidades", verduras)
        _add_item("Tomates", "6 kg", verduras)

        self.treeview.expandAll() # Expandir todos los nodos

        # Recorrer y mostrar en consola
        def dump_item(item: QStandardItem, nivel=0):
            filas = item.rowCount() # Número de filas hijas
            for r in range(filas):
                k = item.child(r, 0) # Clave
                v = item.child(r, 1) # Valor
                print("  " * nivel + f"{k.text()}: {v.text()}") # Mostrar clave y valor
                # Si este 'k' tiene hijos, recorrerlos recursivamente
                if k.hasChildren():
                    dump_item(k, nivel + 1)
        
        # Iniciar recorrido desde el ítem raíz
        for r in range(self.model.rowCount()):
            root_key = self.model.item(r, 0) # Clave raíz
            root_value = self.model.item(r, 1) # Valor raíz
            print(f"- {root_key.text()}: {root_value.text()}") # Mostrar raíz
            if root_key.hasChildren(): # Si tiene hijos, recorrerlos
                dump_item(root_key, 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow("QStandardItemModel - Intro")
    window.show()
    sys.exit(app.exec())