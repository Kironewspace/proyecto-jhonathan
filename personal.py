from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# Configuración de conexión SQL Server
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

# Diccionario para mapear los targets con URLs externas
URL_MAP = {
    "agregar-tareas": "http://127.0.0.1:5003",
    "historial-tareas": "http://127.0.0.1:5003/history",
    "pedidos": "http://127.0.0.1:5005/pedidos",
    "facturas": "http://127.0.0.1:5006/facturas",
}

@app.route("/")
def home():
    return render_template("rutas.html")

@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        target = request.form["target"]

        # Validación de usuario en base de datos
        try:
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                query = """
                SELECT usr_id, usr_name, usr_privileg
                FROM users
                WHERE usr_name = ? AND usr_password = ?
                """
                cursor.execute(query, (username, password))
                user = cursor.fetchone()

                if user:
                    # Redirigir al target si es válido
                    if target in URL_MAP:
                        return redirect(URL_MAP[target])
                    else:
                        return "Destino no válido", 400
                else:
                    return render_template("confirm.html", error="Usuario o contraseña incorrectos", target=target)
        except pyodbc.Error as e:
            return f"Error en la base de datos: {str(e)}"

    # Muestra la página de confirmación
    target = request.args.get("target", "/")
    return render_template("confirm.html", target=target)

if __name__ == "__main__":
    app.run(port=5006, debug=True)
