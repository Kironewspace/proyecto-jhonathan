from flask import Flask, render_template, url_for, redirect
import pyodbc

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

def get_db_connection():
    """Establece una conexión con la base de datos."""
    try:
        return pyodbc.connect(conn_str)
    except pyodbc.Error as e:
        print(f"Error de conexión: {e}")
        return None

@app.route('/facturas')
def listar_facturas():
    """Ruta para listar todas las facturas."""
    conn = get_db_connection()
    if not conn:
        return "Error al conectar a la base de datos", 500

    cursor = conn.cursor()
    query = """
        SELECT f.codigo_factura, f.codigo_pedido, c.nombre AS cliente_nombre, f.nombre_cliente,
               pr.nombre AS producto_nombre, pr.modelo, f.cantidad, f.total, 
               f.fecha_factura, f.fecha_pedido, f.estado
        FROM Factura f
        JOIN Clientes c ON f.id_cliente = c.id_cliente
        JOIN Producto pr ON f.id_producto = pr.id;
    """
    try:
        cursor.execute(query)
        facturas = cursor.fetchall()
    except pyodbc.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        facturas = []
    finally:
        conn.close()

    return render_template('facturas.html', facturas=facturas)

@app.route('/eliminar_factura/<codigo_pedido>')
def eliminar_factura(codigo_pedido):
    """Ruta para eliminar una factura."""
    conn = get_db_connection()
    if not conn:
        return "Error al conectar a la base de datos", 500

    cursor = conn.cursor()

    try:
        # Recuperar cantidad y actualizar stock
        cursor.execute("""
            SELECT id_producto, cantidad FROM Factura WHERE codigo_pedido = ?
        """, (codigo_pedido,))
        factura = cursor.fetchone()

        if factura:
            id_producto, cantidad = factura
            cursor.execute("UPDATE Producto SET stock = stock + ? WHERE id = ?", (cantidad, id_producto))

        # Eliminar factura
        cursor.execute("DELETE FROM Factura WHERE codigo_pedido = ?", (codigo_pedido,))
        conn.commit()
    except pyodbc.Error as e:
        print(f"Error al eliminar la factura: {e}")
        return "Error al eliminar la factura", 500
    finally:
        conn.close()

    return redirect(url_for('listar_facturas'))

if __name__ == '__main__':
    app.run(port=5004, debug=True)
from flask import Flask, render_template, url_for, redirect
import pyodbc

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

def get_db_connection():
    """Establece una conexión con la base de datos."""
    try:
        return pyodbc.connect(conn_str)
    except pyodbc.Error as e:
        print(f"Error de conexión: {e}")
        return None

@app.route('/facturas')
def listar_facturas():
    """Ruta para listar todas las facturas."""
    conn = get_db_connection()
    if not conn:
        return "Error al conectar a la base de datos", 500

    cursor = conn.cursor()
    query = """
        SELECT f.codigo_factura, f.codigo_pedido, c.nombre AS cliente_nombre, f.nombre_cliente,
               pr.nombre AS producto_nombre, pr.modelo, f.cantidad, f.total, 
               f.fecha_factura, f.fecha_pedido, f.estado
        FROM Factura f
        JOIN Clientes c ON f.id_cliente = c.id_cliente
        JOIN Producto pr ON f.id_producto = pr.id;
    """
    try:
        cursor.execute(query)
        facturas = cursor.fetchall()
    except pyodbc.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        facturas = []
    finally:
        conn.close()

    return render_template('facturas.html', facturas=facturas)

@app.route('/eliminar_factura/<codigo_pedido>')
def eliminar_factura(codigo_pedido):
    """Ruta para eliminar una factura."""
    conn = get_db_connection()
    if not conn:
        return "Error al conectar a la base de datos", 500

    cursor = conn.cursor()

    try:
        # Recuperar cantidad y actualizar stock
        cursor.execute("""
            SELECT id_producto, cantidad FROM Factura WHERE codigo_pedido = ?
        """, (codigo_pedido,))
        factura = cursor.fetchone()

        if factura:
            id_producto, cantidad = factura
            cursor.execute("UPDATE Producto SET stock = stock + ? WHERE id = ?", (cantidad, id_producto))

        # Eliminar factura
        cursor.execute("DELETE FROM Factura WHERE codigo_pedido = ?", (codigo_pedido,))
        conn.commit()
    except pyodbc.Error as e:
        print(f"Error al eliminar la factura: {e}")
        return "Error al eliminar la factura", 500
    finally:
        conn.close()

    return redirect(url_for('listar_facturas'))

if __name__ == '__main__':
    app.run(port=5004, debug=True)
