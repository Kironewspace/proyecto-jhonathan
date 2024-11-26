from flask import Flask, render_template, abort, redirect
import pyodbc
import base64

app = Flask(__name__)

# Configuración de conexión a la base de datos
sql_config = {
    'driver': 'ODBC Driver 18 for SQL Server',
    'server': 'localhost',
    'database': 'Darwin',
    'user': 'SA',
    'password': 'MTp070213.'
}
conn_str = (
    f"DRIVER={sql_config['driver']};"
    f"SERVER={sql_config['server']};"
    f"DATABASE={sql_config['database']};"
    f"UID={sql_config['user']};"
    f"PWD={sql_config['password']};"
    "TrustServerCertificate=yes;"
)

# Función para obtener productos por categoría
def obtener_productos(categoria=None):
    productos = []
    query = """
        SELECT id, nombre, modelo, precio, imagen, categoria
        FROM Producto
    """
    if categoria and categoria != "todos":
        query += " WHERE categoria = ?"
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            if categoria and categoria != "todos":
                cursor.execute(query, categoria)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                productos.append({
                    'id': row.id,
                    'nombre': row.nombre,
                    'modelo': row.modelo,
                    'precio': row.precio,
                    'categoria': row.categoria,
                    'imagen': base64.b64encode(row.imagen).decode('utf-8') if row.imagen else None
                })
    except Exception as e:
        print(f"Error al obtener productos: {e}")
    return productos

# Ruta para la página principal (muestra todos los productos)
@app.route('/')
def productos():
    productos = obtener_productos()
    return render_template('showproducts.html', productos=productos, categoria='todos')

# Ruta dinámica para categorías (teléfonos, cargadores, accesorios)
@app.route('/<string:categoria>')
def mostrar_productos_por_categoria(categoria):
    categorias_validas = ['telefono', 'cargador', 'accesorio']
    if categoria not in categorias_validas:
        return abort(404, description="Categoría no válida")

    productos = obtener_productos(categoria)
    return render_template('showproducts.html', productos=productos, categoria=categoria)

# Ruta para detalles del producto
@app.route('/producto/<int:producto_id>')
def producto_detalle(producto_id):
    query = """
        SELECT id, nombre, modelo, especificaciones, precio, stock, imagen 
        FROM Producto
        WHERE id = ?
    """
    producto = None
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, producto_id)
            row = cursor.fetchone()
            if row:
                producto = {
                    'id': row.id,
                    'nombre': row.nombre,
                    'modelo': row.modelo,
                    'especificaciones': row.especificaciones,
                    'precio': row.precio,
                    'stock': row.stock,
                    'imagen': base64.b64encode(row.imagen).decode('utf-8') if row.imagen else None
                }
    except Exception as e:
        print(f"Error al obtener el producto: {e}")
    if producto:
        return render_template('details.html', producto_detalle=producto)
    else:
        return abort(404, description="Producto no encontrado")

# Ruta para redirigir al formulario en la otra aplicación Flask
@app.route('/comprar/<int:producto_id>/<int:cantidad>')
def comprar(producto_id, cantidad):
    return redirect(f'http://127.0.0.1:5002/formulario/{producto_id}/{cantidad}')

# Inicio del servidor
if __name__ == '__main__':
    app.run(debug=True, port=5001)
