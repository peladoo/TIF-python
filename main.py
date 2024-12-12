import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                          VALUES (?, ?, ?, ?, ?)''', (nombre, descripcion, cantidad, precio, categoria))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado al inventario.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos para cantidad y precio.")

# Función para buscar productos
def buscar_producto():
    criterio = simpledialog.askstring("Buscar Producto", "Ingrese el nombre del producto a buscar:")
    if not criterio:
        return
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{criterio}%",))
    productos = cursor.fetchall()
    conn.close()

    if productos:
        resultado = "\n".join([f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: {p[4]}, Categoría: {p[5]}" for p in productos])
        messagebox.showinfo("Resultados de la Búsqueda", resultado)
    else:
        messagebox.showinfo("Resultados de la Búsqueda", "No se encontraron productos con ese nombre.")

# Función para editar un producto
def editar_producto():
    producto_id = simpledialog.askstring("Editar Producto", "Ingrese el ID del producto a editar:")
    if not producto_id:
        return
    try:
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

        if producto:
            nombre = simpledialog.askstring("Editar Producto", "Nombre actual: " + producto[1] + ". Ingrese el nuevo nombre:") or producto[1]
            descripcion = simpledialog.askstring("Editar Producto", "Descripción actual: " + (producto[2] or "") + ". Ingrese la nueva descripción:") or producto[2]
            cantidad = int(simpledialog.askstring("Editar Producto", "Cantidad actual: " + str(producto[3]) + ". Ingrese la nueva cantidad:") or producto[3])
            precio = float(simpledialog.askstring("Editar Producto", "Precio actual: " + str(producto[4]) + ". Ingrese el nuevo precio:") or producto[4])
            categoria = simpledialog.askstring("Editar Producto", "Categoría actual: " + producto[5] + ". Ingrese la nueva categoría:") or producto[5]

            cursor.execute('''UPDATE productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? WHERE id = ?''',
                           (nombre, descripcion, cantidad, precio, categoria, producto_id))
            conn.commit()
            messagebox.showinfo("Éxito", f"Producto con ID {producto_id} actualizado correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró un producto con ese ID.")
        conn.close()
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

# Función para eliminar un producto del inventario
def eliminar_producto():
    producto_id = simpledialog.askstring("Eliminar Producto", "Ingrese el ID del producto a eliminar:")
    if not producto_id:
        return
    try:
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", f"Producto con ID {producto_id} eliminado del inventario.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")

# Función para mostrar el inventario completo
def mostrar_inventario():
    inventario_ventana = tk.Toplevel(ventana)
    inventario_ventana.title("Inventario Completo")
    inventario_ventana.geometry("800x600")

    columnas = ("ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría")
    tree = ttk.Treeview(inventario_ventana, columns=columnas, show="headings", height=20)
    tree.pack(side="left", fill="both", expand=True)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    scrollbar = ttk.Scrollbar(inventario_ventana, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    for producto in productos:
        tree.insert("", "end", values=producto)

# Función para registrar una venta y descontar del inventario
def registrar_venta():
    producto_id = simpledialog.askstring("Registrar Venta", "Ingrese el ID del producto vendido:")
    if not producto_id:
        return
    try:
        cantidad_vendida = int(simpledialog.askstring("Registrar Venta", "Ingrese la cantidad vendida:"))
        if cantidad_vendida < 0:
            messagebox.showerror("Error", "La cantidad vendida no puede ser negativa.")
            return

        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad, precio, nombre FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

        if producto:
            cantidad_actual, precio, nombre_producto = producto
            if cantidad_vendida > cantidad_actual:
                messagebox.showerror("Error", "La cantidad vendida excede el inventario disponible.")
                return

            nueva_cantidad = cantidad_actual - cantidad_vendida
            monto_total = cantidad_vendida * precio
            cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, producto_id))
            conn.commit()
            messagebox.showinfo("Éxito", f"Venta registrada.\nProducto: {nombre_producto}\nCantidad vendida: {cantidad_vendida}\nCantidad restante: {nueva_cantidad}\nMonto total: ${monto_total:.2f}")
        else:
            messagebox.showerror("Error", "No se encontró un producto con ese ID.")

        conn.close()
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")
    producto_id = simpledialog.askstring("Registrar Venta", "Ingrese el ID del producto vendido:")
    if not producto_id:
        return
    try:
        cantidad_vendida = int(simpledialog.askstring("Registrar Venta", "Ingrese la cantidad vendida:"))
        if cantidad_vendida < 0:
            messagebox.showerror("Error", "La cantidad vendida no puede ser negativa.")
            return

        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad, nombre FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

        if producto:
            cantidad_actual = producto[0]
            nombre_producto = producto[1]
            if cantidad_vendida > cantidad_actual:
                messagebox.showerror("Error", "La cantidad vendida excede el inventario disponible.")
                return

            nueva_cantidad = cantidad_actual - cantidad_vendida
            cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, producto_id))
            conn.commit()
            messagebox.showinfo("Éxito", f"Venta registrada. Producto: {nombre_producto}, Cantidad vendida: {cantidad_vendida}, Cantidad restante: {nueva_cantidad}.")
        else:
            messagebox.showerror("Error", "No se encontró un producto con ese ID.")

        conn.close()
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Inventario de Ferretería")
ventana.geometry("400x400")

# Crear botones para las opciones
btn_agregar = ttk.Button(ventana, text="Agregar Producto", command=agregar_producto)
btn_agregar.pack(pady=5)

btn_buscar = ttk.Button(ventana, text="Buscar Producto", command=buscar_producto)
btn_buscar.pack(pady=5)

btn_editar = ttk.Button(ventana, text="Editar Producto", command=editar_producto)
btn_editar.pack(pady=5)

btn_eliminar = ttk.Button(ventana, text="Eliminar Producto", command=eliminar_producto)
btn_eliminar.pack(pady=5)

btn_mostrar = ttk.Button(ventana, text="Mostrar Inventario", command=mostrar_inventario)
btn_mostrar.pack(pady=5)

btn_venta = ttk.Button(ventana, text="Registrar Venta", command=registrar_venta)
btn_venta.pack(pady=5)

btn_salir = ttk.Button(ventana, text="Salir", command=ventana.quit)
btn_salir.pack(pady=5)

# Ejecutar el bucle principal
ventana.mainloop()
