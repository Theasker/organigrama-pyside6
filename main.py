import sys
from siu2dict_openpyxl import SIU_to_dict
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel, QProgressBar, QStatusBar, QTreeView, 
                               QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QPushButton, 
                               QLineEdit, QHeaderView, QFileDialog)
from PySide6.QtCore import QModelIndex, QRegularExpression, Qt, QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPalette, QColor, QIcon

URL = "https://aplicaciones.aragon.es/siu_admin/download_descargar"

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Organigrama Gobierno de Aragón")
        self.resize(1200, 600)
        self.setWindowIcon(QIcon("assets/genfavicon-package/genfavicon-256.png"))

        # Variables para la búsqueda
        self.total_organismos = 0
        self.find_results = [] # Lista de índices que coinciden con la búsqueda
        self.current_findex = -1 # Índice actual en la lista de resultados

        # Variable para filtrado por niveles
        self.datos_originales = None # Para guardar los datos originales sin filtrar

        self._create_widgets()
        self._create_layout()
        self._set_dark_palette() # Configura la paleta antes del estilo CSS
        self._create_connections()
        self._create_style()

    def _load_initial_data(self):
        # Comprobamos si está el xlsx localmente, si no, lo descargamos y descomprimimos
        siu = SIU_to_dict(URL)
        if not siu.existe_local():
            self.status_bar.showMessage("Descargando datos por primera vez (esto puede tardar un poco)...")
            # Forzamos a la interfaz a mostrar el mensaje antes de bloquearse
            QApplication.processEvents()
            
            if not siu.descargar_zip(siu.url):
                self.status_bar.showMessage("Error al descargar los datos. Revisa tu conexión a internet.")
                return # Salimos para no intentar descomprimir ni procesar el Excel si la descarga falló
            
            if not siu.descomprimir_zip():
                self.status_bar.showMessage("Error al descomprimir los datos descargados.")
                return # Salimos para no intentar procesar el Excel si la descompresión falló
            
        # Procesamos los datos (ya sea descargados o los que ya estaban)
        self.status_bar.showMessage("Procesando datos...", 1000)
        QApplication.processEvents()

        datos_raw = siu.procesar_excel_ligero()

        if datos_raw:
            self.status_bar.showMessage("Creando árbol de datos...", 1000)
            QApplication.processEvents()

            dct = siu.crear_arbol(datos_raw)
            self.datos_originales = dct # Guardamos los datos originales
            self._make_tree(dct)

            self.status_bar.showMessage("Datos cargados correctamente.")
        else:
            self.status_bar.showMessage("No se pudo cargar el Excel.")

    def _reload_data(self):
        # Función para recargar los datos desde el Excel (después de una actualización)
        
        # Reset de variables para la búsqueda
        self.total_organismos = 0 # Reiniciamos el contador de organismos
        self.find_results = [] # Lista de índices que coinciden con la búsqueda
        self.current_findex = -1 # Índice actual en la lista de resultados

        self.model.clear() # Limpiamos el modelo actual
        self.model.setHorizontalHeaderLabels(["Código", "Organismo"]) # Volvemos a establecer las cabeceras

        # Si existe, borramos el contenido del directorio tmp para forzar a descargar el nuevo Excel
        # borrar directiorio tmp
        import shutil
        import os
        if os.path.exists("tmp"):
            shutil.rmtree("tmp")
        self._load_initial_data() # Volvemos a cargar los datos (esto forzará a descargar el nuevo Excel y procesarlo)

    def _create_widgets(self):
        # QTreeView para mostrar el organigrama _____________________________________
        self.tree_view = QTreeView()
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setIndentation(20)
        self.tree_view.header().setMinimumSectionSize(50) # Asegura que la primera columna no sea minúscula
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
        # FIN QTreeView _______________________________________________________________
        
        # Cuadro de búsqueda
        self.frame_find = QFrame()
        self.find_box = QLineEdit()
        self.find_box.setPlaceholderText("Buscar...")
        # self.find_box.setFixedSize(200, 22)  # Tamaño fijo para el cuadro de búsqueda
        self.find_box.setClearButtonEnabled(True)  # Botón para limpiar el texto

        self.find_next_button = QPushButton(">")
        # self.find_next_button.setFixedSize(20, 22)
        self.find_next_button.setEnabled(False)

        self.find_prev_button = QPushButton("<")
        # self.find_prev_button.setFixedSize(20, 22)
        self.find_prev_button.setEnabled(False)

        self.find_label_items = QLabel("0/0")  # Etiqueta para mostrar el número de resultados y la posición actual
        self.find_label_items.setFixedSize(40, 22)         

        # Cuadro de filtrado
        self.filter_box = QLineEdit()
        self.filter_box.setPlaceholderText("Filtrar...")
        self.filter_box.setClearButtonEnabled(True)  # Botón para limpiar el texto

        self.filter_label_items = QLabel("0/0")  # Etiqueta para mostrar el número de resultados y la posición actual
        self.filter_label_items.setFixedSize(60, 22)

        # Nivel a mostrar
        self.lbl_levels = QLabel("Niveles:")
        self.combo_levels = QComboBox()
        self.combo_levels.addItems(["Todos", "1", "2", "3", "4"])
        self.combo_levels.setCurrentIndex(0) # Por defecto, mostrar todos los niveles

        # Agrupar y expandir arbol
        self.button_expand = QPushButton("🔻")
        self.button_expand.setChecked(True)  # Por defecto, el árbol está expandido
        self.button_collapse = QPushButton("🔺")

        # Botón de recargar
        self.button_reload = QPushButton("⭯")
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Iniciando aplicación...")

        # Versión
        self.label_version = QLabel("v0.1.0 | Mauricio Segura Ariño (mseguraa@aragon.es)")
        self.status_bar.addPermanentWidget(self.label_version) # Añade la etiqueta de versión a la derecha de la barra de estado

    def _create_layout(self):
        # Contenedor principal (widget central del QMainWindow)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout horizontal para los cuadros de texto
        layoutH = QHBoxLayout()
        layoutV = QVBoxLayout()
        
        layoutV.addLayout(layoutH) # Añadimos el layout horizontal al vertical
        # layout.addWidget(self.progress_bar)        

        self.frame_find = QFrame() # Creamos un marco para agrupar los elementos de búsqueda
        self.frame_find.setObjectName("frameVerde") # Para aplicar estilos específicos al marco de búsqueda
        layout_find = QHBoxLayout(self.frame_find)
        layout_find.addWidget(self.find_box)
        layout_find.addWidget(self.find_prev_button)
        layout_find.addWidget(self.find_next_button)
        layout_find.addWidget(self.find_label_items)
        layoutH.addWidget(self.frame_find)

        self.frame_filter = QFrame() # Creamos un marco para agrupar los elementos de filtrado
        self.frame_filter.setObjectName("frameAzul") # Para aplicar estilos específicos al marco
        layout_filter = QHBoxLayout(self.frame_filter)
        layout_filter.addWidget(self.filter_box)
        layout_filter.addWidget(self.filter_label_items)
        layoutH.addWidget(self.frame_filter)

        layoutH.addWidget(self.lbl_levels)
        layoutH.addWidget(self.combo_levels)

        # Crear un marco que engloba los botones de expandir y colapsar para que estén juntos
        layoutH.addWidget(self.button_expand)
        layoutH.addWidget(self.button_collapse)

        layoutH.addWidget(self.button_reload)

        
        layoutV.addWidget(self.tree_view)
    
        # IMPORTANTE: El layout se pone en el central_widget, NO en self
        self.central_widget.setLayout(layoutV) # Establecemos el layout vertical como el layout
      
    def _set_dark_palette(self):
        # Configuramos una paleta oficial para que el sistema sepa que estamos en modo oscuro
        # Esto hace que elementos nativos (como las flechas del árbol) se dibujen claros
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(61, 61, 61))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(37, 37, 37))
        dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.black)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(85, 85, 85))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(255, 152, 0)) # Naranja highlight
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        QApplication.setPalette(dark_palette)

    def _create_style(self):
        # Estilo general oscuro
        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #3d3d3d; color: #E0E0E0; font-family: 'Segoe UI'; }
            QLineEdit, QComboBox { background-color: #4f4f4f; border: 1px solid #969696; padding: 4px; color: white; }
                           
            QPushButton { background-color: #969696; color: #3d3d3d; border-radius: 4px; font-weight: bold; padding: 5px; }
            
            /* Igualar tamaño de los botones */
            QPushButton { min-width: 22px; min-height: 22px; }
                           
            /* Modo oscuro de titulo del QTreeView sin borde transparente */
            QHeaderView::section { background-color: #454545; color: #E0E0E0; border: 1px solid #969696; padding: 2px; }
                                          
            /* Labels centrados */
            QLabel { qproperty-alignment: 'AlignCenter'; background-color: #454545 }
            /* Estilo para el label de versión*/
            QLabel#labelVersion { font-size: 10px; color: gray; margin-right: 10px;}

            /* Estilo de los marcos */
            QFrame#frameVerde { border: 2px solid #A5D6A7; border-radius: 8px; background-color: #454545; }
            QFrame#frameAzul { border: 2px solid #90CAF9; border-radius: 8px; background-color: #454545; }

                           
            /* --- QTreeView Styling (Nuevo) --- */
            QTreeView {
                background-color: #252525;
                alternate-background-color: #2d2d2d;
                border: 1px solid #333;
                selection-background-color: #ff9800;
                selection-color: black;
                outline: none;
                font-size: 13px;
                /* Sin flechas personalizadas en el CSS para dejar que la QPalette las maneje nativamente */
            }
            
            QTreeView::item {
                height: 24px;
                padding-left: 5px;
            }
            
            QTreeView::item:hover {
                background-color: #3d3d3d;
            }
            
            QTreeView::item:selected {
                background-color: #ff9800;
                color: black;
            }

            /* Estilo para el editor (cuando se edita una celda) */
            QTreeView QLineEdit {
                background-color: #ffffff;
                color: #333333;
                padding: 0px;
                margin: 0px;
                border: 1px solid #ff9800;
            }
        """)

    def _create_connections(self):
        # Señales para el cuadro de texto de filtrado
        self.filter_box.textChanged.connect(self._filter_tree) 
        # Señales para el cuadro de texto de búsqueda
        self.find_box.textChanged.connect(self._find_in_tree)        
        self.find_next_button.clicked.connect(self._next_result)
        self.find_prev_button.clicked.connect(self._prev_result)
        # Señales para los botones de expandir y colapsar
        self.combo_levels.currentIndexChanged.connect(self._on_level_change) # Señal para cambio de nivel a mostrar
        self.button_expand.clicked.connect(self.tree_view.expandAll)
        self.button_collapse.clicked.connect(self.tree_view.collapseAll)  
        self.button_reload.clicked.connect(self._reload_data) # Recarga los datos al hacer clic en el botón de recargar     

    def _filter_tree(self, text):
        if text:
            # Usar expresión regular para buscar el texto en cualquier parte
            text = QRegularExpression.escape(text)  # Escapa caracteres especiales para que se busquen literalmente
            self.proxy_model.setFilterRegularExpression(f".*{text}.*")
            # Actualiza la búsqueda para que se vuelva a calcular la lista de resultados con el nuevo filtro
            self._find_in_tree(self.find_box.text())
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
        # Buscamos desde la columna 0 (Código)
        # Al usar MatchRecursive, Qt buscará en toda la jerarquía.
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

            self.status_bar.showMessage(f"Resultado {self.current_findex + 1} de {len(self.find_results)}")

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

    def _make_tree(self, dct, limite_nivel=None):
        # 1. Limpiamos el modelo y contadores antes de empezar
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Código", "Organismo"])
        self.total_organismos = 0

        # 2. Nueva función recursiva con control de profundidad
        def recursive(element, parent_item, nivel_actual=0):
            # Si hay límite y lo hemos superado, dejamos de procesar hijos
            if limite_nivel is not None and nivel_actual > limite_nivel:
                return

            if isinstance(element, dict):
                code_item = QStandardItem(element.get("codigo", ""))
                name_item = QStandardItem(element.get("nombre", ""))
                parent_item.appendRow([code_item, name_item])
                self.total_organismos += 1 # Contador de organismos

                # Solo seguimos con los hijos si no hemos llegado al límite
                for child in element.get("hijos", []):
                    recursive(child, code_item, nivel_actual + 1)
            elif isinstance(element, list):
                for item in element:
                    recursive(item, parent_item, nivel_actual)     
        
        # 3. Lanzamos la recursión (empezamos en nivel 0 para la raíz)
        recursive(dct, self.model.invisibleRootItem(), 0)

        self.tree_view.expandAll()
        self.tree_view.resizeColumnToContents(0)
        self.tree_view.resizeColumnToContents(1)

    def _on_level_change(self):
        if not self.datos_originales:
            return # Si no tenemos datos cargados, no hacemos nada
        
        limite_nivel = self.combo_levels.currentText()

        if limite_nivel == "Todos":
            limite_nivel = None
        else:
            limite_nivel = int(limite_nivel) - 1 # Porque el nivel 1 es el índice 0 en la función recursiva
        
        # Reconstruimos el árbol desde los datos fuente
        self._make_tree(self.datos_originales, limite_nivel=limite_nivel)
        
        # Opcional: Si había un filtro de texto aplicado, lo relanzamos
        self._filter_tree(self.filter_box.text())

if __name__ == "__main__":
        # siu = SIU_to_dict(URL)
        # dct = siu.arbol_completo
        app = QApplication(sys.argv)
        app.setStyle("Fusion") # Estilo común para mejor soporte de QSS
        window = Mainwindow()
        window.show()
        window._load_initial_data()
        sys.exit(app.exec())
       