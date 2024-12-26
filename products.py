from flask import Flask, request, redirect, url_for, render_template
import pyodbc

app = Flask(__name__)


sql_config = {
    'driver': 'ODBC Driver 18 for SQL Server',
    'server': 'localhost',
    'database': 'DarwinCell',
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
    "Encrypt=no;"
)


@app.route('/productos')
def mostrar_productos():
    return render_template('products.html')

def agregar_producto(nombre, modelo, especificaciones, categoria, tipo_accesorio, stock, precio, imagen):
    query = """INSERT INTO Productos 
               (nombre, modelo, especificaciones, categoria, tipo_accesorio, stock, precio, imagen)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nombre, modelo, especificaciones, categoria, tipo_accesorio, stock, precio, imagen))
            conn.commit()
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos:", e)


@app.route('/agregar_producto', methods=['POST'])
def agregar_producto_form():
    data = request.form
    nombre = data['productname']
    modelo = data['productmodel']
    especificaciones = data['productspecs']
    categoria = data['productcategory']
    tipo_accesorio = data['accessorytype'] if categoria == 'accesorio' else None
    stock = int(data['productStock'])
    precio = float(data['productPrice'])
    imagen = request.files['productimage'].read()  

    agregar_producto(nombre, modelo, especificaciones, categoria, tipo_accesorio, stock, precio, imagen)

    return redirect(url_for('producto_agregado'))


@app.route('/producto_agregado')
def producto_agregado():
    return "Producto agregado exitosamente."

if __name__ == '__main__':
    app.run(port=5009, debug=True)
