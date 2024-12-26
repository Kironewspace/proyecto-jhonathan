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

# Conexión a la base de datos
conn_str = (
    f"DRIVER={sql_config['driver']};SERVER={sql_config['server']};DATABASE={sql_config['database']};UID={sql_config['user']};PWD={sql_config['password']};TrustServerCertificate=yes;"
)


# Función para obtener las tareas pendientes
def get_pending_todos():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tareas WHERE status = 'Pending'")
    todos = cursor.fetchall()
    conn.close()
    return todos

# Función para obtener las tareas completadas
def get_completed_todos():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tareas WHERE status = 'Completed'")
    todos = cursor.fetchall()
    conn.close()
    return todos

# Función para agregar una tarea a la base de datos
def add_todo(title, description, priority):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tareas (title, description, priority, status) VALUES (?, ?, ?, ?)", 
                   (title, description, priority, 'Pending'))
    conn.commit()
    conn.close()

# Función para eliminar una tarea de la base de datos
def delete_todo(todo_id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()

# Función para actualizar el estado de una tarea
def update_status(todo_id, status):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("UPDATE tareas SET status = ? WHERE id = ?", (status, todo_id))
    conn.commit()
    conn.close()

# Ruta principal para mostrar la lista de tareas pendientes
@app.route('/')
def index():
    todos = get_pending_todos()
    return render_template('todo.html', todos=todos)

# Ruta para el historial de tareas completadas
@app.route('/history')
def history():
    completed_todos = get_completed_todos()
    return render_template('historial.html', todos=completed_todos)

# Ruta para agregar una nueva tarea
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')
    add_todo(title, description, priority)
    return redirect(url_for('index'))

# Ruta para eliminar una tarea
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    delete_todo(todo_id)
    return redirect(url_for('index'))

# Ruta para cambiar el estado de una tarea
@app.route('/update_status/<int:todo_id>/<string:status>')
def update_status_route(todo_id, status):
    update_status(todo_id, status)
    if status == 'Completed':
        return redirect(url_for('index'))
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)
