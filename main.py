import sys
import json
from siu2dict import SIU_to_dict
from PySide6.QtWidgets import (QApplication, QLabel, QProgressBar, QTreeView, QVBoxLayout, QHBoxLayout,
                               QMainWindow, QWidget, QPushButton, QLineEdit, QHeaderView)
from PySide6.QtCore import QModelIndex, QRegularExpression, Qt, QSortFilterProxyModel
# Importación para el modelo de datos del QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem

class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Organigrama Gobierno de Aragón")
        self.resize(1100, 600)
        # Variables para la búsqueda
        self.total_organismos = 0
        self.find_results = [] # Lista de índices que coinciden con la búsqueda
        self.current_findex = -1 # Índice actual en la lista de resultados
        
        self._create_widgets()
        self._create_layout()
        self._create_connections()

    def _create_widgets(self):
        # self.progress_bar = QProgressBar()
        # self.progress_bar.setRange(0, 100)
        self.tree_view = QTreeView()
        self.tree_view.resizeColumnToContents(0) # expande la primera columna (código)
        # Creamos el modelo de qtreeview que es el contenedor de los datos que se van a mostrar en el treeview
        
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Código", "Organismo"])
        
        # Creamos el proxy model para filtrar
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)  # No distingue mayúsculas
        self.proxy_model.setFilterKeyColumn(-1)  # Busca en todas las columnas
        self.proxy_model.setRecursiveFilteringEnabled(True)  # IMPORTANTE: filtra recursivamente en la jerarquía

        # El QTreeView muestra el proxy, no el modelo directo
        self.tree_view.setModel(self.proxy_model)
        
        # Cuadro de búsqueda
        self.find_box = QLineEdit()
        self.find_box.setPlaceholderText("Buscar...")
        self.find_box.setFixedSize(200, 22)  # Tamaño fijo para el cuadro de búsqueda
        self.find_box.setClearButtonEnabled(True)  # Botón para limpiar el texto

        self.find_next_button = QPushButton(">")
        self.find_next_button.setFixedSize(20, 22)
        self.find_next_button.setEnabled(False)

        self.find_prev_button = QPushButton("<")
        self.find_prev_button.setFixedSize(20, 22)
        self.find_prev_button.setEnabled(False)

        self.find_label_items = QLabel("0/0")  # Etiqueta para mostrar el número de resultados y la posición actual
        self.find_label_items.setFixedSize(40, 22)         

        # Cuadro de filtrado
        self.filter_box = QLineEdit()
        self.filter_box.setPlaceholderText("Filtrar...")
        self.filter_box.setClearButtonEnabled(True)  # Botón para limpiar el texto

        self.filter_label_items = QLabel("0/0")  # Etiqueta para mostrar el número de resultados y la posición actual
        self.filter_label_items.setFixedSize(60, 22)

        # Agrupar y expandir arbol
        self.button_expand = QPushButton("🔻")
        self.button_expand.setChecked(True)  # Por defecto, el árbol está expandido
        self.button_collapse = QPushButton("🔺")

    def _create_layout(self):
        # Layout horizontal para los cuadros de texto
        layoutH = QHBoxLayout()
        layoutV = QVBoxLayout()
        
        layoutV.addLayout(layoutH) # Añadimos el layout horizontal al vertical
        # layout.addWidget(self.progress_bar)        

        layoutH.addWidget(self.find_box)
        layoutH.addWidget(self.find_prev_button)
        layoutH.addWidget(self.find_next_button)
        layoutH.addWidget(self.find_label_items)

        layoutH.addWidget(self.filter_box)
        layoutH.addWidget(self.filter_label_items)
        # Crear un marco que engloba los botones de expandir y colapsar para que estén juntos
        layoutH.addWidget(self.button_expand)
        layoutH.addWidget(self.button_collapse)

        self.setLayout(layoutV)
        layoutV.addWidget(self.tree_view)
        self.setLayout(layoutV)
      
    def _create_connections(self):
        # Señales para el cuadro de texto de filtrado
        self.filter_box.textChanged.connect(self._filter_tree) 
        # Señales para el cuadro de texto de búsqueda
        self.find_box.textChanged.connect(self._find_in_tree)        
        self.find_next_button.clicked.connect(self._next_result)
        self.find_prev_button.clicked.connect(self._prev_result)
        # Señales para los botones de expandir y colapsar
        self.button_expand.clicked.connect(self.tree_view.expandAll)
        self.button_collapse.clicked.connect(self.tree_view.collapseAll)       

    def _filter_tree(self, text):
        if text:
            # Usar expresión regular para buscar el texto en cualquier parte
            text = QRegularExpression.escape(text)  # Escapa caracteres especiales para que se busquen literalmente
            self.proxy_model.setFilterRegularExpression(f".*{text}.*")
        else:
            # Si está vacío, mostrar todo
            self.proxy_model.setFilterRegularExpression("")
        
        visibles = self._count_visible_items(None)

        # ¿Cómo calculamos el TOTAL absoluto? 
        # El sourceModel() siempre tiene todos los datos.
        # Pero ojo, el sourceModel también es un árbol, así que 
        # necesitarías otra función igual para el total real o 
        # guardarlo en una variable cuando cargas el JSON.

        self.filter_label_items.setText(f"{visibles}/{self.total_organismos}")

        self.tree_view.expandAll()  # Expande automáticamente para mostrar resultados

    def _count_visible_items(self, parent_index):
        # Si el índice es None, empezamos desde la raíz del proxy model
        if parent_index is None:
            parent_index = QModelIndex() # Creamos el índice raíz (vacío) para el proxy model
        # Función recursiva para contar los elementos visibles 
        # en el proxy model (después de aplicar el filtro)
        count = self.proxy_model.rowCount(parent_index)
        total = count # Empezamos contando los hijos directos visibles
        for row in range(count):
            # Obtenemos el índice del hijo en el proxy model
            child_index = self.proxy_model.index(row, 0, parent_index)
            # Sumamos sus propios hijos visibles (recursivamente)
            total += self._count_visible_items(child_index)
        return total

    def _find_in_tree(self, text):
        # Si no hay texto, limpiamos los resultados y reseteamos el índice
        if not text:
            self.find_results = []
            self.current_findex = -1 # Índice actual en la lista de resultados
            self.find_label_items.setText("0/0")
            # Desactivamos los botones de siguiente/anterior
            self.find_next_button.setEnabled(False)
            self.find_prev_button.setEnabled(False)
            return
        
        # Obtenemos el índice de inicio (fila 0, columna 0 del PROXY)
        start_index = self.proxy_model.index(0, 1)

        # Llamamos a match para obtener una lista de índices que coinciden con el texto en cualquier parte (columna -1)
        self.find_results = self.proxy_model.match(
            start_index, # índice de inicio
            Qt.DisplayRole, # buscamos en el texto mostrado
            text, # el texto a buscar
            -1, # número máximo de coincidencias a devolver (-1 para todas)
            Qt.MatchContains | Qt.MatchRecursive # buscamos coincidencias que contengan el texto y que se busquen recursivamente en toda la jerarquía
        )

        # Obtenemos la lista de resultados de la búsqueda
        if self.find_results:
            self.current_findex = 0
            # Imprime para debuggear en consola
            print(f"Encontrados: {len(self.find_results)}")
            # Llamamos a una función que mueva el "foco" al primer resultado
            self._update_selection() 
        else:
            self.current_findex = -1
            self.find_label_items.setText("0/0")
        
        # Activamos o desactivamos los botones de siguiente/anterior según si hay resultados
        hay_resultados = len(self.find_results) > 0
        print(f"Hay resultados: {hay_resultados}")
        self.find_next_button.setEnabled(hay_resultados)
        self.find_prev_button.setEnabled(hay_resultados)
    
    # Función para actualizar la selección en el QTreeView según el resultado actual de la búsqueda
    def _update_selection(self):
        # Mueve el foco al resultado actual 
        # y actualiza la etiqueta con el número de resultados y la posición actual
        if 0 <= self.current_findex < len(self.find_results):
            target_index = self.find_results[self.current_findex] # Índice del resultado actual

            # Le decimos a la vista: "Selecciona este índice"
            self.tree_view.setCurrentIndex(target_index)

            # Le decimos a la vista: "Haz scroll hasta que se vea"
            self.tree_view.scrollTo(target_index, QTreeView.PositionAtCenter)

            # Actualizamos la etiqueta con el número de resultados y la posición actual
            self.find_label_items.setText(f"{self.current_findex + 1}/{len(self.find_results)}")

    def _next_result(self):
        # Siguiente resultado: incrementamos el índice y actualizamos la selección
        if self.find_results:
            # Incrementamos y usamos el resto de la división para volver a 0 al llegar al final
            self.current_findex = (self.current_findex + 1) % len(self.find_results)
            print(f"Siguiente: {self.current_findex + 1}/{len(self.find_results)}")
            self._update_selection()

    def _prev_result(self):
        # Salta al resultado anterior de búsqueda.
        if self.find_results:
            # En Python, el módulo con números negativos funciona de cine:
            # (0 - 1) % 5 devuelve 4. Directo al último.
            self.current_findex = (self.current_findex - 1) % len(self.find_results)
            self._update_selection()

    def _make_tree(self, dct):
        # Función recursiva para llenar el modelo a partir del diccionario
        def recursive(element, parent_item):
            if isinstance(element, dict):
                code_item = QStandardItem(element.get("codigo", ""))
                name_item = QStandardItem(element.get("nombre", ""))
                parent_item.appendRow([code_item, name_item])
                for child in element.get("hijos", []):
                    recursive(child, code_item)
                # Contador de organismos
                self.total_organismos += 1
            elif isinstance(element, list):
                for item in element:
                    recursive(item, parent_item)
            
        
        # Llenamos el modelo con los datos del diccionario
        recursive(dct, self.model.invisibleRootItem())
        # Estira la primera columna para mostrar el código completo
        self.tree_view.expandAll()
        self.tree_view.resizeColumnToContents(0)
        self.tree_view.resizeColumnToContents(1)   

if __name__ == "__main__":
        URL = "https://aplicaciones.aragon.es/siu_admin/download_descargar"
        siu = SIU_to_dict(URL)
        dct = siu.arbol_completo

        if dct is not None:
            app = QApplication([])
            window = Mainwindow()
            window.show()
            window._make_tree(dct)
            sys.exit(app.exec())
        else:
            print("No se ha podido cargar el DataFrame")
            sys.exit(1)