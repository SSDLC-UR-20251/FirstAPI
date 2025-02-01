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


# Obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Actualización parcial de una tarea
@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def patch_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        abort(404, description="Tarea no encontrada")
    data = request.json
    task.update({
        key: data[key] for key in data if key in task
    })
    save_data()
    return jsonify(task)

# Filtrar las tareas completadas
@app.route('/completedTask', methods = ['GET'])
def get_filter_tasks():
    filterTask = []
    for taski in tasks:
        if taski["completed"] == True:
            filterTask.append(taski)
    return jsonify(filterTask)

# Obtener todas las tareas de una categoria
@app.route('/getCategories/<int:category_id>/tasks', methods = ['GET'])
def get_categories_tasks(category_id):
    categoriesTasks = []
    for taski in tasks:
        if taski["category_id"] == category_id:
            categoriesTasks.append(taski)
    return jsonify(categoriesTasks)

# Eliminar una tarea
@app.route('/tasks/<int:id>', methods = ['DELETE'])
def deleteTask(id):
    for taski in tasks:
        if taski["id"] == id:
            tasks.remove(taski)
    return jsonify(tasks)

# Eliminar una categoria
@app.route('/categories/<int:id>', methods = ['DELETE'])
def deleteCategorie(id):
    for taski in categories:
        if taski["id"] == id:
            categories.remove(taski)
    return jsonify(categories)

# Crear una nueva tarea
@app.route('/tasks', methods=['POST'])
def post_task():
    data = request.json
    return jsonify(task)
    


if __name__ == '__main__':
    app.run(debug=True)
