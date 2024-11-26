import pyodbc
from flask import Flask, render_template, request

sql_config = {
    'driver': 'ODBC Driver 18 for SQL Server',
    'server': 'localhost',
    'database': 'Darwin',
    'user': 'SA',
    'password': 'MTp070213.'
}

conn = pyodbc.connect(
    f"DRIVER={sql_config['driver']};SERVER={sql_config['server']};DATABASE={sql_config['database']};UID={sql_config['user']};PWD={sql_config['password']};TrustServerCertificate=yes;"
)

app = Flask(__name__)

@app.route('/')
def show():
    return render_template("users.html")

@app.route("/users", methods=['POST'])
def submit():
    usr_name = request.form.get('username')
    usr_password = request.form.get('usr_password')
    usr_privilegy = request.form.get('privilegio')
    db_password = request.form.get('especialpassword')

    cursor = conn.cursor()
    db_pass_row = cursor.execute("SELECT db_password FROM db_admin").fetchone()
    db_pass = db_pass_row[0] if db_pass_row else None

    if db_password == db_pass:
        existing_user = cursor.execute("SELECT COUNT(*) FROM users WHERE usr_name = ?", (usr_name,)).fetchone()[0]
        
        if existing_user > 0:
            cursor.close()
            return "El usuario ya existe en la base de datos."
        else:
            cursor.execute("INSERT INTO users (usr_name, usr_password, usr_privileg) VALUES (?, ?, ?)", (usr_name, usr_password, usr_privilegy))
            cursor.commit()
            cursor.close()
            return "Usuario agregado con éxito."
    else:
        cursor.close()
        return "No puedes agregar un usuario debido a que no posees el privilegio adecuado."


if __name__ == '__main__':
    app.run(port=50010, debug=True)
