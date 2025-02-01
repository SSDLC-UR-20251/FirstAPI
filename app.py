import json
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Cargar datos desde un archivo JSON
def load_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"categories": [], "tasks": []}

# Guardar datos en el archivo JSON
def save_data():
    with open('data.json', 'w') as file:
        json.dump({"categories": categories, "tasks": tasks}, file, indent=4)

data = load_data()
categories = data["categories"]
tasks = data["tasks"]


# Obtener todas las categorías
@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(categories)

# Obtener todas las tareas de un categoria
@app.route('/categories/<int:category_id>/tasks', methods=['GET'])
def get_categories_task(category_id):
    tareas = []
    for i in tasks:
        if (i['category_id']) == category_id: tareas.append(i['title'])
    return jsonify(tareas)

# Obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Obtener todas las tareas completas
@app.route('/tasks/completed=true', methods=['GET'])
def get_tasks_completed():
    tareas = []
    for i in tasks:
        if i["completed"] == True: tareas.append(i['title'])
    return jsonify(tareas)

# Actualización parcial de una tarea
@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def patch_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        abort(404, description="Tarea no encontrada")
    data = request.json
    for y in data: tarea = y
    if tarea == "completed":
        if (type(data['completed'])) != bool:
            abort(400, description="Debe ser un Booleano")
    task.update({
        key: data[key] for key in data if key in task
    })
    save_data()
    return jsonify(task)

#Crear nueva tarea
@app.route('/tasks', methods=['POST'])
def post_task():
    task = next((task for task in tasks if task["id"] == "task_id"), None)
    if task is None:
        abort(404, description="Tarea no encontrada")
    data = request.json
    task.update({
        key: data[key] for key in data if key in task
    })
    save_data()
    return jsonify(task)

if __name__ == '__main__':
    app.run(debug=True)
