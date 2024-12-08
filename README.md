Inventario de Ferretería
Autor: Mauricio Martin Fontana
Este programa es una aplicación de escritorio para gestionar el inventario de productos de una ferretería. Fue desarrollado en Python utilizando tkinter para la interfaz gráfica y sqlite3 para la base de datos.

Funcionalidades
El programa permite realizar las siguientes acciones:

Agregar productos:
Añadir nuevos productos al inventario especificando nombre, descripción, cantidad, precio y categoría.

Mostrar inventario:
Visualizar todos los productos registrados en el inventario, incluyendo sus detalles como ID, nombre, descripción, cantidad, precio y categoría.

Eliminar productos:
Eliminar un producto del inventario utilizando su ID.

Actualizar productos:
Modificar la cantidad y el precio de un producto existente en el inventario.

Buscar productos:
Buscar un producto por su nombre y obtener información detallada del mismo.

Reporte de bajo stock:
Generar un informe de productos con stock igual o inferior a un valor límite definido por el usuario.

Salir:
Cerrar la aplicación de manera segura.

Requisitos Previos
Python 3.x instalado en tu sistema.
Puedes descargar Python desde python.org.

Biblioteca tkinter incluida en Python por defecto.

Biblioteca sqlite3, también incluida por defecto en Python.

Instalación y Uso
Clona o descarga este repositorio:

bash
Copiar código
git clone <url-del-repositorio>
cd inventario-ferreteria
Ejecuta el programa:
Abre una terminal o consola en la carpeta donde está ubicado el archivo del programa y ejecuta:

bash
Copiar código
python inventario.py
Interfaz gráfica:
Una ventana se abrirá mostrando las opciones principales del programa. Desde allí, podrás interactuar con el inventario.

Cómo Ver la Base de Datos
La base de datos se guarda en un archivo llamado inventario.db. Puedes explorarla usando:

Herramientas gráficas:

DB Browser for SQLite
SQLiteStudio
Línea de comandos de SQLite:

Navega al directorio del proyecto y usa:
bash
Copiar código
sqlite3 inventario.db
Consulta los datos con:
sql
Copiar código
SELECT * FROM productos;
Desde el programa Python:
Ejecuta la función ver_productos() incluida en el código para listar los productos en la consola.

Posibles Mejoras Futuras
Implementar filtros avanzados para buscar productos por categoría o rango de precios.
Exportar el inventario a formatos como Excel o PDF.
Incorporar autenticación para acceso seguro al inventario.
Si tienes alguna duda o sugerencia, ¡no dudes en contactarme!

Desarrollado por [Tu Nombre y Apellido]
