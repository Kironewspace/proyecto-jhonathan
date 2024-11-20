from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import random

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

# Ruta para mostrar el formulario de cliente
@app.route('/formulario/<int:producto_id>/<int:cantidad>', methods=['GET', 'POST'])
def formulario_cliente(producto_id, cantidad):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        email = request.form.get('email')

        # Generar un código de pedido
        codigo_pedido = 'UF-' + ''.join([str(random.randint(0, 9)) for _ in range(6)])

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Guardar al cliente en la tabla Clientes
            cursor.execute(
                """
                INSERT INTO Clientes (nombre, telefono, email)
                VALUES (?, ?, ?)
                """,
                (nombre, telefono, email)
            )
            id_cliente = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

            # Obtener el nombre del producto para el pedido
            cursor.execute("SELECT nombre FROM Productos WHERE id = ?", producto_id)
            producto = cursor.fetchone()
            if not producto:
                return "Producto no encontrado", 404

            nombre_producto = producto[0]

            # Guardar el pedido en la tabla Pedido
            cursor.execute(
                """
                INSERT INTO Pedido (codigo_pedido, id_cliente, nombre_cliente, id_producto, cantidad)
                VALUES (?, ?, ?, ?, ?)
                """,
                (codigo_pedido, id_cliente, nombre, producto_id, cantidad)
            )
            conn.commit()
        except Exception as e:
            return f"Error al guardar el pedido: {e}", 500
        finally:
            conn.close()

        # Redirigir al endpoint correcto: agradecimiento
        return redirect(url_for('agradecimiento', codigo_pedido=codigo_pedido))
    return render_template('shop.html', producto_id=producto_id, cantidad=cantidad)

# Ruta para mostrar la página de agradecimiento
@app.route('/agradecimiento/<codigo_pedido>')
def agradecimiento(codigo_pedido):
    return render_template('thanks.html', codigo_pedido=codigo_pedido)

if __name__ == '__main__':
    app.run(port=5002, debug=True)
