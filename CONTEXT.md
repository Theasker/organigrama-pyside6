# Resumen del Proyecto: Visualizador de Organigrama (PySide6)

Este documento sirve como memoria técnica y contexto de desarrollo para el visualizador de la estructura orgánica del Gobierno de Aragón.

## 1. Arquitectura de Datos
* **Fuente**: JSON jerárquico obtenido de una URL de administración.
* **Estructura**: Diccionario con claves `codigo`, `nombre` e `hijos` (lista de diccionarios).
* **Modelo**: `QStandardItemModel` con 2 columnas: "Código" y "Organismo".
* **Procesamiento**: Carga recursiva mediante `_make_tree`, que además calcula el `total_organismos` base para el contador global.

## 2. Componentes de Interfaz y Lógica
### Vista y Filtrado
* **Control**: `QSortFilterProxyModel` para desacoplar los datos reales de la visualización.
* **Filtrado Jerárquico**: Configurado con `setRecursiveFilteringEnabled(True)` para que, al filtrar un hijo, sus padres permanezcan visibles.
* **Conteo Dinámico**: Método `_count_visible_items` que recorre el proxy recursivamente usando `rowCount(parent_index)` para obtener cuántos elementos pasan el filtro actual.

### Sistema de Búsqueda y Navegación
* **Motor**: Uso de `proxy_model.match()` con los flags `Qt.MatchContains | Qt.MatchRecursive`.
* **Navegación Circular**: Implementada mediante **aritmética modular** para los botones `<` y `>`.
    * Siguiente: `(indice + 1) % total`.
    * Anterior: `(indice - 1) % total`.
* **Sincronización**: El método `_filter_tree` invoca a `_find_in_tree` para que los resultados de búsqueda se actualicen automáticamente según lo que el filtro permite ver.

## 3. Lógica de Navegación (Aritmética Modular)

Para permitir que el usuario navegue en bucle por los resultados de búsqueda:

- **Siguiente Resultado**:
  `self.current_findex = (self.current_findex + 1) % len(self.find_results)`.
- **Resultado Anterior**:
  `self.current_findex = (self.current_findex - 1) % len(self.find_results)`.

## 4. Implementación de Búsqueda Estable (Columna 1)

El método `_find_in_tree` realiza las siguientes acciones:
1. Limpia resultados y desactiva botones si el texto está vacío.
2. Define el punto de inicio en la columna 1 (Organismo) para una búsqueda precisa: `start_index = self.proxy_model.index(0, 1)`.
3. Ejecuta `match()` de forma recursiva en todo el árbol visible.
4. Actualiza la etiqueta `find_label_items` con el formato "Actual/Total".
5. Habilita o deshabilita los botones de navegación según la existencia de coincidencias.

## 5. Historial de Git
* **Commit Inicial**: Configuración de `.gitignore`, inicialización del repositorio y carga de la lógica base de filtrado y búsqueda funcional.