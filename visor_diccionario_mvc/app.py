
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTreeView, QLabel
)
from PySide6.QtGui import QStandardItemModel
from PySide6.QtCore import Qt

# MODELO (M de MVC)
class BaseKeyValueModel(QStandardItemModel):
    """
    Modelo base con dos columnas: 'Clave' y 'Valor'.
    De momento no contiene datos. Sirve para validar la conexión vista <-> modelo.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_headers()

    def _setup_headers(self):
        self.setHorizontalHeaderLabels(["Clave", "Valor"])

    # Nota: más adelante aquí crearemos un modelo especializado para dict/list,
    # con populate() recursivo y metadatos (ruta del nodo, etc.).

# VISTA (V de MVC)
class MainWindow(QMainWindow):
    """
    Ventana principal que contiene la vista (QTreeView) y elementos de UI.
    No conoce 'cómo' se cargan los datos; solo sabe mostrar un modelo.
    """
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._setup_tree()

    def _setup_ui(self):
        self.setWindowTitle("Inventario | Visor de diccionario — Paso 1 (MVC en un archivo)")
        self.resize(900, 600)

        # Widget central y layout vertical
        self._central = QWidget(self)
        self._layout = QVBoxLayout(self._central)
        self.setCentralWidget(self._central)

        # Pista visual (texto superior)
        hint = QLabel("Vista QTreeView conectada a un modelo vacío (dos columnas).")
        hint.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._layout.addWidget(hint)

        # Barra de estado
        self.statusBar().showMessage("Inicializando...")

    def _setup_tree(self):
        self.tree = QTreeView(self)
        # Ajustes visuales razonables
        self.tree.setAlternatingRowColors(True)
        self.tree.setUniformRowHeights(True)   # rendimiento con muchos nodos
        self.tree.header().setStretchLastSection(True)
        self.tree.header().setDefaultSectionSize(320)
        self._layout.addWidget(self.tree)

    # Método de conveniencia para que el controlador inyecte el modelo
    def set_model(self, model: QStandardItemModel):
        self.tree.setModel(model)
        self.statusBar().showMessage("Vista en árbol conectada a modelo base (sin datos)")

# CONTROLADOR (C de MVC)
class AppController:
    """
    Orquesta la aplicación: crea el modelo, lo conecta a la vista,
    y (en pasos posteriores) gestionará eventos, búsqueda, edición, etc.
    """
    def __init__(self, window: MainWindow):
        self.window = window
        self.model = None

    def start(self):
        # 1) Crear el modelo base (vacío)
        self.model = BaseKeyValueModel()

        # 2) Conectar el modelo a la vista
        self.window.set_model(self.model)

        # 3) (Más adelante) conectar señales, cargar datos, etc.
        #    Hoy NO cargamos datos aún: solo estructura.



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    controller = AppController(window)
    controller.start()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
