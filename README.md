# Inventario de Ferretería

### Autor: **Mauricio Martin Fontana**

Este programa es una aplicación de escritorio para gestionar el inventario de productos de una ferretería. Fue desarrollado en Python utilizando `tkinter` para la interfaz gráfica y `sqlite3` para la base de datos.

---

## Funcionalidades

El programa permite realizar las siguientes acciones:

1. **Agregar productos**:  
   Añadir nuevos productos al inventario especificando nombre, descripción, cantidad, precio y categoría.

2. **Mostrar inventario**:  
   Visualizar todos los productos registrados en el inventario, incluyendo sus detalles como ID, nombre, descripción, cantidad, precio y categoría.

3. **Eliminar productos**:  
   Eliminar un producto del inventario utilizando su ID.

4. **Actualizar productos**:  
   Modificar la cantidad y el precio de un producto existente en el inventario.

5. **Buscar productos**:  
   Buscar un producto por su nombre y obtener información detallada del mismo.

6. **Reporte de bajo stock**:  
   Generar un informe de productos con stock igual o inferior a un valor límite definido por el usuario.

7. **Salir**:  
   Cerrar la aplicación de manera segura.

---

## Requisitos Previos

- **Python 3.x** instalado en tu sistema.  
  Puedes descargar Python desde [python.org](https://www.python.org/).

- Biblioteca **`tkinter`**, incluida en Python por defecto.

- Biblioteca **`sqlite3`**, también incluida por defecto en Python.

---

## Instalación y Uso

1. **Clona o descarga este repositorio**:

   ```bash
   git clone https://github.com/peladoo/TIF-python.git
   cd TIF-python

   ```

2. **Ejecuta el programa**:  
   Abre una terminal o consola en la carpeta donde está ubicado el archivo del programa y ejecuta:
   python inventario.py

3. **Interactua con el programa**:
   Utiliza las funcionalidades que te ofrezcan el programa para gestionar tu inventario de productos de ferretería.

---

## Cómo Ver la Base de Datos

La base de datos se guarda en un archivo llamado `inventario.db`. Puedes explorarla usando cualquiera de las siguientes opciones:

### Herramientas gráficas

- [DB Browser for SQLite](https://sqlitebrowser.org/)
- [SQLiteStudio](https://sqlitestudio.pl/)

### Línea de comandos de SQLite

1. **Navega al directorio del proyecto y abre una terminal**.
2. **Usa el siguiente comando para acceder a la base de datos**:
   ```bash
   sqlite3 inventario.db
   ```
3. **Consulta los datos con la instrucción SQL**:
   ```sql
   SELECT * FROM productos;
   ```

## Posibles Mejoras Futuras

- Implementar filtros avanzados para buscar productos por categoría o rango de precios.
- Exportar el inventario a formatos como Excel o PDF.
- Incorporar autenticación para garantizar un acceso seguro al inventario.
