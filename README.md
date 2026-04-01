# Organigrama App (PySide6)

Aplicación de ejemplo para cargar un árbol jerárquico desde un dict (SIU/JSON) en `QTreeView` usando `PySide6`.

## 📦 Estructura

- `qtreeview03_carga DataFrame.py`: interfaz principal y lógica de inserción + filtrado + búsqueda/navegación.
- `siu2dict.py`: conversor de datos SIU a diccionario Python.
- `Organigrama_actual.txt`, `backup/`, `tmp/`, etc.: datos de soporte/historicos.
- `requirements.txt`: dependencias.

## ⚙️ Requisitos

- Python 3.10+ (o 3.11)
- PySide6

Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

> Si no existe `requirements.txt`, instala manualmente:
>
> ```bash
> python -m pip install PySide6
> ```

## ▶️ Ejecutar

```bash
cd c:\Users\mseguraa\Documents\Python\organigrama_app
.venv-1\Scripts\python.exe "qtreeview03_carga DataFrame.py"
```

O si usas un entorno global:

```bash
python "qtreeview03_carga DataFrame.py"
```

## 🧩 Funcionalidades incluidas

- Carga recursiva de datos jerárquicos (`codigo`, `nombre`, `hijos`) en un `QStandardItemModel`.
- Filtrado reactivo con `QSortFilterProxyModel` (recursivo, case-insensitive).
- Buscador `find_box` + navegación `next/prev` + contador.
- Expansión y colapso de todo el árbol.
- Autofit de columnas con `resizeColumnToContents`.

## 🛠️ Cómo funciona el buscador

- `find_box.textChanged` dispara `_find_in_tree`.
- `_find_in_tree` crea una lista `self.find_results` de índices coincidentes.
- `_find_next` / `_find_prev` recorren `find_results` y actualizan selección con `_select_current_result`.

## 🧪 Pruebas rápidas

- Busca `agricultura` en el campo filtro -> debe mostrar solo los nodos que contienen ese texto.
- Busca en el campo `find_box` (el buscador) -> número de coincidencias actualizado en etiqueta `items_lbl`, navegación posible con `<` `>`.

## 🔍 Mejoras futuras

- Marcar visualmente el nodo activo con background color temporal.
- Buscar por regex configurable.
- Exportar nodo seleccionado/filtrado a JSON/CSV.

## 📌 Notas

- La funcionalidad de filtro y la de navegación están separadas: usas filtro para ocultar y búsqueda para recorrer coincidencias.
- Si la URL de SIU no responde, carga datos locales de `Organigrama_actual.txt` en formato JSON/dict antes de ejecutar.
