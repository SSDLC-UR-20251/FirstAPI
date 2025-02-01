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

# Filtrar tareas completadas
@app.route('/tasks/completed', methods=['GET'])
def get_task_completed():
    task_completed = [task for task in tasks if task['completed']]
    return jsonify(task_completed)

# Obtener todas las tareas de una categoría
@app.route('/categories/<int:category_id>/tasks', methods=['GET'])
def get_tasks_category(category_id):
    tasks_cat = [task for task in tasks if task['category_id'] == category_id]
    return jsonify(tasks_cat)

# Eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task_to_delete = None
    for task in tasks:
        if task['id'] == task_id :
            task_to_delete = task
            break
    if task_to_delete:
        tasks.remove(task_to_delete)
        return '', 204
    else:
        return {'message': 'Task not found'}, 404

# Agregar una tarea
@app.route('/tasks', methods=['POST'])
def new_task():
    task_data = request.get_json

    if not task_data or task_data['title'] not in task_data or task_data['category_id'] not in task_data:
        return {'message': 'Missing required fields (title, category_id)'}, 400

    new_task = {
        'id': len(tasks) + 1,  
        'title': task_data['title'],
        'completed': task_data.get('completed', False), 
        'category_id': task_data['category_id']
    }

    tasks.append(new_task)
    return jsonify(new_task), 201


if __name__ == '__main__':
    app.run(debug=True)
