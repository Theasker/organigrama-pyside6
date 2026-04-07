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
        self.info.setText("Ejercicio 9: árbol con metadatos (roles), edición y señales.")

        PATH_ROLE = Qt.UserRole + 1 # Rol personalizado para ruta oculta
        
        # Crea un nodo padre "Departamentos"
        dep = QStandardItem("Departamentos")
        dep_value = QStandardItem("")
        self.model.appendRow([dep, dep_value])

        # Hijo "Tecnología" con dos pares clave-valor
        tech = QStandardItem("Tecnología")
        tech_value = QStandardItem("")
        dep.appendRow([tech, tech_value])

        # Fila1 bajo "Tecnología"
        k1, v1 = QStandardItem("responsable"), QStandardItem("Maurcio Segura")
        # Guarda ruta oculta en ambos items (ej: ["departamentos", "Tecnología", "responsable"])
        ruta1 = ["departamentos", "Tecnología", "responsable"]
        k1.setData(ruta1, PATH_ROLE) # Guardar ruta en rol personalizado
        v1.setData(ruta1, PATH_ROLE) # Guardar ruta en rol personalizado
        v1.setEditable(True)  # Hacer editable el valor
        tech.appendRow([k1, v1])

        # Fila 2 bajo Tecnología
        k2, v2 = QStandardItem("equipo"), QStandardItem("3 personas")
        # Guarda ruta oculta en ambos items (ej: ["departamentos", "Tecnología", "equipo"])
        ruta2 = ["departamentos", "Tecnología", "equipo"]
        k2.setData(ruta2, PATH_ROLE) # Guardar ruta en rol personalizado
        v2.setData(ruta2, PATH_ROLE) # Guardar ruta en rol personalizado
        v2.setEditable(True)  # Hacer editable el valor
        tech.appendRow([k2, v2])

        self.treeview.expandAll() # Expandir todo el árbol
        self.model.itemChanged.connect(self.on_item_changed_meta(PATH_ROLE)) # Conectar señal de cambio

    def on_item_changed_meta(self, PATH_ROLE):
        # Devolvemos una faunción (closure) que recuerda el PATH_ROLE
        def handler(item: QStandardItem):
            if item.column() != 1:
                return  # Solo procesar cambios en la columna de valor
            ruta = item.data(PATH_ROLE) # Obtener ruta oculta
            print(f"[SEÑAL] Cambiado {ruta} => '{item.text()}'") # Mostrar cambio
        return handler

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow("QStandardItemModel - Intro")
    window.show()
    sys.exit(app.exec())