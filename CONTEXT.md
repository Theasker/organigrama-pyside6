# Resumen del Proyecto: Visualizador de Organigrama (PySide6)

## 1. Arquitectura de Datos y Vista (Estado Actual)
* **Modelo/Proxy**: `QStandardItemModel` (Código, Organismo) gestionado por `QSortFilterProxyModel` con filtrado recursivo.
* **Búsqueda/Navegación**: Sincronizada con el filtro, usando `match()` y aritmética modular para el bucle de resultados.
* **Clase Base**: Actualmente `QWidget`.

## 2. Nuevos Objetivos de Desarrollo
### A. Refactorización a QMainWindow
* **Motivo**: Obtener acceso nativo a `StatusBar`, `MenuBar` y una gestión de layouts más profesional.
* **Cambio**: Heredar de `QMainWindow` y establecer un `setCentralWidget`.

### B. Sistema de Descarga e Hilos (Multithreading)
* **Problema**: La descarga/descompresión bloquea el hilo principal (GUI), dejando la aplicación "congelada".
* **Solución**: Implementar `QThread` con una clase `Worker`.
* **Comunicación**: Uso de **Signals y Slots** para enviar el % de progreso desde el hilo de descarga a la barra de progreso de la interfaz.

### C. Exportación Visual
* **Formato**: PDF jerárquico.
* **Librería**: ReportLab (aprovechando experiencia previa del usuario).
* **Lógica**: Recorrido recursivo del `proxy_model` para mantener la indentación visual en el documento.

## 3. Lógica de Sincronización Filtro-Búsqueda
* El método `_filter_tree` llama a `_find_in_tree` para asegurar que el usuario solo navegue por elementos visibles tras el filtrado.