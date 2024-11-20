from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import base64

app = Flask(__name__)

# Configuración de conexión
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

def get_db_connection():
    return pyodbc.connect(conn_str)

# Ruta principal: muestra los productos
@app.route('/')
def productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, modelo, precio, imagen FROM Productos")
    productos = cursor.fetchall()
    conn.close()

    productos_con_imagen = []
    for prod in productos:
        img_data = base64.b64encode(prod.imagen).decode('utf-8') if prod.imagen else None
        productos_con_imagen.append({
            'id': prod.id,
            'nombre': prod.nombre,
            'modelo': prod.modelo,
            'precio': prod.precio,
            'imagen': img_data,
        })

    return render_template('showproducts.html', productos=productos_con_imagen)

# Ruta para mostrar detalles del producto
@app.route('/producto/<int:producto_id>', methods=['GET', 'POST'])
def producto_detalle(producto_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, modelo, especificaciones, precio, stock, imagen FROM Productos WHERE id = ?", producto_id)
    producto = cursor.fetchone()
    conn.close()

    if producto:
        img_data = base64.b64encode(producto.imagen).decode('utf-8') if producto.imagen else None
        producto_info = {
            'id': producto_id,
            'nombre': producto.nombre,
            'modelo': producto.modelo,
            'especificaciones': producto.especificaciones,
            'precio': producto.precio,
            'stock': producto.stock,
            'imagen': img_data,
        }
        return render_template('details.html', producto=producto_info)
    else:
        return "Producto no encontrado", 404

# Ruta para redirigir al formulario en la otra aplicación Flask
@app.route('/comprar/<int:producto_id>/<int:cantidad>')
def comprar(producto_id, cantidad):
    return redirect(f'http://127.0.0.1:5002/formulario/{producto_id}/{cantidad}')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
