import sys
from siu2dict import SIU_to_dict
from PySide6.QtWidgets import QApplication, QMainWindow, QProgressBar, QTreeView, QVBoxLayout, QWidget, QPushButton
# Importación para el modelo de datos del QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem

class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Organigrama Gobierno de Aragón")
        self.resize(400, 300)
        self._create_widgets()
        self._create_layout()
        #self._create_connections()

    def _create_widgets(self):
        # self.progress_bar = QProgressBar()
        # self.progress_bar.setRange(0, 100)
        self.tree_view = QTreeView()
        self.tree_view.expandAll()
        self.tree_view.resizeColumnToContents(0) # expande la primera columna (código)

        # Creamos el modelo de qtreeview que es el contenedor de los datos que se van a mostrar en el treeview
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Código", "Organismo"])

        # Creamos el item "Padre"
        parent_col0 = QStandardItem("ORG00001")
        parent_col1 = QStandardItem("GOBIERNO DE ARAGÓN")
        
        # Añadimos el ítem "Padre" al modelo
        self.model.appendRow([parent_col0, parent_col1])

        # Creamos un ítem "Hijo" y lo añadimos al ítem "Padre"
        child_col0 = QStandardItem("ORG00002")
        child_col1 = QStandardItem("Departamento de Educación")
        parent_col0.appendRow([child_col0, child_col1])
      

        # Conectamos el modelo a la vista
        self.tree_view.setModel(self.model)
       
    
    def _create_layout(self):
        layout = QVBoxLayout()
        # layout.addWidget(self.progress_bar)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)


if __name__ == "__main__":
        app = QApplication([])
        window = Mainwindow()
        window.show()
        sys.exit(app.exec())