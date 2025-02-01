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
    
    task_to_delete = next((task for task in tasks if task['id'] == task_id), None)
    if not task_to_delete:
        return {'message': 'Task not found'}, 404
    
    tasks.remove(task_to_delete)    
    save_data()
    return '', 204

# Agregar una tarea
@app.route('/tasks', methods=['POST'])
def new_task():
    task_data = request.json

    # Validar campos requeridos
    if not task_data or 'title' not in task_data or 'category_id' not in task_data:
        return {'message': 'Faltan campos requeridos (title, category_id)'}, 400

    title = task_data['title'].strip()
    category_id = task_data['category_id']
    completed = task_data.get('completed', False)

    # Validar longitud del título
    if not (3 <= len(title) <= 100):
        return {'message': 'El título debe tener entre 3 y 100 caracteres'}, 400

    # Validar que el título no se repita en la misma categoría
    if any(task['title'].lower() == title.lower() and task['category_id'] == category_id for task in tasks):
        return {'message': 'Ya existe una tarea con ese título en la misma categoría'}, 400

    # Validar que category_id exista
    if not any(cat['id'] == category_id for cat in categories):
        return {'message': 'category_id inválido'}, 400

    # Validar que completed sea booleano
    if not isinstance(completed, bool):
        return {'message': 'El campo completed debe ser booleano (true o false)'}, 400

    new_id = max([task['id'] for task in tasks], default=0) + 1
    new_task = {
        'id': new_id,
        'title': title,
        'completed': completed,
        'category_id': category_id
    }

    tasks.append(new_task)
    save_data()
    return jsonify(new_task), 201

# Crear una nueva categoría
@app.route('/categories', methods=['POST'])
def new_category():
    category_data = request.json

    if not category_data or 'name' not in category_data:
        return {'message': 'Falta el campo requerido (name)'}, 400

    name = category_data['name'].strip()

    # Validar que el nombre no esté vacío
    if not name:
        return {'message': 'El nombre de la categoría no puede estar vacío'}, 400

    # Validar que el nombre de la categoría no se repita (case insensitive)
    if any(cat['name'].lower() == name.lower() for cat in categories):
        return {'message': 'Ya existe una categoría con ese nombre'}, 400

    new_id = max([cat['id'] for cat in categories], default=0) + 1
    new_category = {
        'id': new_id,
        'name': name
    }

    categories.append(new_category)
    save_data()
    return jsonify(new_category), 201

# Actualizar una tarea
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return {'message': 'Tarea no encontrada'}, 404

    task_data = request.json
    title = task_data.get('title', task['title']).strip()
    category_id = task_data.get('category_id', task['category_id'])
    completed = task_data.get('completed', task['completed'])

    if not (3 <= len(title) <= 100):
        return {'message': 'El título debe tener entre 3 y 100 caracteres'}, 400

    if any(t['title'].lower() == title.lower() and t['category_id'] == category_id and t['id'] != task_id for t in tasks):
        return {'message': 'Ya existe una tarea con ese título en la misma categoría'}, 400

    if not any(cat['id'] == category_id for cat in categories):
        return {'message': 'category_id inválido'}, 400

    if not isinstance(completed, bool):
        return {'message': 'El campo completed debe ser booleano (true o false)'}, 400

    task.update({'title': title, 'category_id': category_id, 'completed': completed})
    save_data()
    return jsonify(task)

# Actualizar una categoría
@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = next((cat for cat in categories if cat["id"] == category_id), None)
    if category is None:
        return {'message': 'Categoría no encontrada'}, 404

    category_data = request.json
    name = category_data.get('name', category['name']).strip()

    if not name:
        return {'message': 'El nombre de la categoría no puede estar vacío'}, 400

    if any(cat['name'].lower() == name.lower() and cat['id'] != category_id for cat in categories):
        return {'message': 'Ya existe una categoría con ese nombre'}, 400

    category['name'] = name
    save_data()
    return jsonify(category)



if __name__ == '__main__':
    app.run(debug=True)
