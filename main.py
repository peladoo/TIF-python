import tkinter as tk
from tkinter import messagebox, simpledialog

import sqlite3

# Crear la base de datos y la tabla de productos si no existe
def crear_base_de_datos():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        descripcion TEXT,
                        cantidad INTEGER NOT NULL,
                        precio REAL NOT NULL,
                        categoria TEXT NOT NULL)''')
    conn.commit()
    conn.close()

crear_base_de_datos()


# Lista para el inventario
inventario = []

# Función para agregar un producto al inventario
def agregar_producto():
    nombre = simpledialog.askstring("Agregar Producto", "Ingrese el nombre del producto:")
    descripcion = simpledialog.askstring("Agregar Producto", "Ingrese la descripción del producto:")
    if not nombre:
        return
    try:
        cantidad = int(simpledialog.askstring("Agregar Producto", "Ingrese la cantidad del producto:"))
        precio = float(simpledialog.askstring("Agregar Producto", "Ingrese el precio del producto:"))
        categoria = simpledialog.askstring("Agregar Producto", "Ingrese la categoría del producto:")
        if cantidad < 0 or precio < 0:
            messagebox.showerror("Error", "La cantidad y el precio no pueden ser negativos.")
            return
        # Conectar a la base de datos e insertar el producto
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                          VALUES (?, ?, ?, ?, ?)''', (nombre, descripcion, cantidad, precio, categoria))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado al inventario.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos para cantidad y precio.")

# Función para mostrar el inventario
def mostrar_inventario():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    if not productos:
        messagebox.showinfo("Inventario", "El inventario está vacío.")
        return
    inventario_texto = "\n".join(
        f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: ${producto[4]}, Categoría: {producto[5]}"
        for producto in productos
    )
    messagebox.showinfo("Inventario", inventario_texto)

# Función para eliminar un producto del inventario
def eliminar_producto():
    producto_id = simpledialog.askstring("Eliminar Producto", "Ingrese el ID del producto que desea eliminar:")
    if not producto_id:
        return
    try:
        producto_id = int(producto_id)
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", f"Producto con ID {producto_id} eliminado del inventario.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")

# Función para actualizar un producto
def actualizar_producto():
    producto_id = simpledialog.askstring("Actualizar Producto", "Ingrese el ID del producto que desea actualizar:")
    if not producto_id:
        return
    try:
        producto_id = int(producto_id)
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

        if producto:
            nueva_cantidad = int(simpledialog.askstring("Actualizar Producto", "Ingrese la nueva cantidad:"))
            nuevo_precio = float(simpledialog.askstring("Actualizar Producto", "Ingrese el nuevo precio:"))
            cursor.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?", 
                           (nueva_cantidad, nuevo_precio, producto_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"Producto con ID {producto_id} actualizado.")
        else:
            conn.close()
            messagebox.showerror("Error", "Producto no encontrado.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

def reporte_bajo_stock():
    limite = simpledialog.askstring("Reporte Bajo Stock", "Ingrese el límite de stock:")
    if not limite:
        return
    try:
        limite = int(limite)
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
        productos_bajo_stock = cursor.fetchall()
        conn.close()

        if productos_bajo_stock:
            reporte = "\n".join(
                f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[3]}, Precio: ${producto[4]}"
                for producto in productos_bajo_stock
            )
            messagebox.showinfo("Reporte Bajo Stock", reporte)
        else:
            messagebox.showinfo("Reporte Bajo Stock", "No hay productos con bajo stock.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número válido para el límite.")

# Función para buscar un producto
def buscar_producto():
    nombre = simpledialog.askstring("Buscar Producto", "Ingrese el nombre del producto que desea buscar:")
    if not nombre:
        return
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    productos = cursor.fetchall()
    conn.close()

    if productos:
        inventario_texto = "\n".join(
            f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: ${producto[4]}, Categoría: {producto[5]}"
            for producto in productos
        )
        messagebox.showinfo("Producto Encontrado", inventario_texto)
    else:
        messagebox.showerror("Error", "Producto no encontrado en el inventario.")


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Inventario de Ferretería")

# Crear botones para las opciones
btn_agregar = tk.Button(ventana, text="Agregar Producto", command=agregar_producto)
btn_agregar.pack(pady=10)

btn_mostrar = tk.Button(ventana, text="Mostrar Inventario", command=mostrar_inventario)
btn_mostrar.pack(pady=10)

btn_eliminar = tk.Button(ventana, text="Eliminar Producto", command=eliminar_producto)
btn_eliminar.pack(pady=10)

btn_actualizar = tk.Button(ventana, text="Actualizar Producto", command=actualizar_producto)
btn_actualizar.pack(pady=10)

btn_buscar = tk.Button(ventana, text="Buscar Producto", command=buscar_producto)
btn_buscar.pack(pady=10)

btn_salir = tk.Button(ventana, text="Salir", command=ventana.quit)
btn_salir.pack(pady=10)

# Ejecutar el bucle principal
ventana.mainloop()
