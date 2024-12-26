from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

sql_config = {
    'driver': 'ODBC Driver 18 for SQL Server',
    'server': 'Miguel-PC',
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
)

def get_db_connection():
    return pyodbc.connect(conn_str)

@app.route('/pedidos')
def listar_pedidos():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT p.codigo_pedido, c.nombre, c.telefono, pr.nombre AS producto_nombre, 
               pr.modelo, p.cantidad, (pr.precio * p.cantidad) AS total
        FROM Pedido p
        JOIN Clientes c ON p.id_cliente = c.id_cliente
        JOIN Productos pr ON p.id_producto = pr.id
        WHERE p.estado = 'Pendiente';
    """
    cursor.execute(query)
    pedidos = cursor.fetchall()
    conn.close()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/confirmar_pedido/<codigo_pedido>')
def confirmar_pedido(codigo_pedido):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Obtener los detalles del pedido (id_producto y cantidad)
        cursor.execute("""
            SELECT id_producto, cantidad 
            FROM Pedido 
            WHERE codigo_pedido = ?
        """, (codigo_pedido,))
        pedido = cursor.fetchone()

        if not pedido:
            return "Pedido no encontrado", 404

        id_producto, cantidad = pedido

        # Disminuir el stock del producto
        cursor.execute("""
            UPDATE Productos 
            SET stock = stock - ? 
            WHERE id = ? AND stock >= ?
        """, (cantidad, id_producto, cantidad))

        if cursor.rowcount == 0:
            return "Error: No hay suficiente stock disponible", 400

        # Insertar el pedido confirmado en la tabla Factura
        cursor.execute("""
            INSERT INTO Factura (codigo_factura, codigo_pedido, id_cliente, nombre_cliente, id_producto, cantidad, total, fecha_factura, fecha_pedido, estado)
            SELECT p.codigo_pedido, p.codigo_pedido, p.id_cliente, c.nombre AS nombre_cliente, p.id_producto, p.cantidad, 
                   (pr.precio * p.cantidad), GETDATE(), p.fecha_pedido, 'Completado'
            FROM Pedido p
            JOIN Clientes c ON p.id_cliente = c.id_cliente
            JOIN Productos pr ON p.id_producto = pr.id
            WHERE p.codigo_pedido = ?
        """, (codigo_pedido,))

        # Eliminar el pedido de la tabla Pedido
        cursor.execute("DELETE FROM Pedido WHERE codigo_pedido = ?", (codigo_pedido,))

        # Confirmar los cambios
        conn.commit()

    except Exception as e:
        conn.rollback()
        return f"Error al confirmar el pedido: {e}", 500
    finally:
        conn.close()

    return redirect(url_for('listar_pedidos'))

@app.route('/eliminar_pedido/<codigo_pedido>')
def eliminar_pedido(codigo_pedido):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Pedido WHERE codigo_pedido = ?", (codigo_pedido,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_pedidos'))

if __name__ == '__main__':
    app.run(port=5003, debug=True)
