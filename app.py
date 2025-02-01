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


#Creacion de tarea
@app.route('/tasks/create_task', methods=['POST'])
def create_task():
    data = request.json
    tasks.append(data)
    save_data()
    return jsonify(tasks)
  

#Creacion de categoria
@app.route('/categories/create_category', methods=['POST'])
def create_category():
    data = request.json
    categories.append(data)
    save_data()
    return jsonify(categories)

#Actualizar tarea
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        abort(404, description="Tarea no encontrada")
    data = request.json
    task.update(data)
    save_data()
    return jsonify(tasks)

#Actualizar categoria
@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = next((category for category in categories if category["id"] == category_id), None)
    if category is None:
        abort(404, description="Categoria no encontrada")
    data = request.json
    category.update(data)
    save_data()
    return jsonify(categories)

#Eliminar tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        abort(404, description="Tarea no encontrada")
    tasks.remove(task)
    save_data()
    return jsonify(tasks)

#Eliminar categoria
@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = next((category for category in categories if category["id"] == category_id), None)
    if category is None:
        abort(404, description="Tarea no encontrada")
    categories.remove(category)
    save_data()
    return jsonify(categories)
    

if __name__ == '__main__':
    app.run(debug=True)
