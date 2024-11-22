import pyodbc
from flask import Flask, render_template, request, redirect, url_for

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
                    return redirect(url_for(target))
                else:
                    return render_template("confirm.html", error="Usuario o contraseña incorrectos", target=target)
        except pyodbc.Error as e:
            return f"Error en la base de datos: {str(e)}"

    # Muestra la página de confirmación
    target = request.args.get("target", "/")
    return render_template("confirm.html", target=target)

@app.route("/agregar-tareas")
def agregar_tareas():
    return "Página para agregar tareas"

@app.route("/historial-tareas")
def historial_tareas():
    return "Página de historial de tareas"

@app.route("/pedidos")
def pedidos():
    return "Página de pedidos"

@app.route("/facturas")
def facturas():
    return "Página de facturas"

if __name__ == "__main__":
    app.run(port=5006, debug=True)
