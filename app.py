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

#--------EJERCICIOS DE CLASE-------------

# Actualización parcial de una tarea con validaciones
@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def patch_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        abort(404, description="Tarea no encontrada")
    
    data = request.json
    
    # Validar título
    if "title" in data:
        title = data["title"].strip()
        if not (3 <= len(title) <= 100):
            abort(400, description="El título debe tener entre 3 y 100 caracteres")
        if any(t["title"].lower() == title.lower() and t["category_id"] == task["category_id"] for t in tasks if t["id"] != task_id):
            abort(400, description="El título ya existe en esta categoría")
        task["title"] = title
    
    # Validar completed
    if "completed" in data:
        if not isinstance(data["completed"], bool):
            abort(400, description="El campo 'completed' debe ser un booleano")
        task["completed"] = data["completed"]
    
    # Validar category_id
    if "category_id" in data:
        if not any(c["id"] == data["category_id"] for c in categories):
            abort(400, description="La categoría especificada no existe")
        task["category_id"] = data["category_id"]
    
    save_data()
    return jsonify(task)


#CREAR UNA TAREA:

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data.get("title", "").strip()
    category_id = data.get("category_id")
    completed = data.get("completed")

    # Validaciones
    if not title or not (3 <= len(title) <= 100):
        abort(400, description="El título debe tener entre 3 y 100 caracteres")
    
    if any(t["title"].lower() == title.lower() and t["category_id"] == category_id for t in tasks):
        abort(400, description="El título ya existe en esta categoría")
    
    if not isinstance(completed, bool):
        abort(400, description="El campo 'completed' debe ser un booleano")
    
    if not any(c["id"] == category_id for c in categories):
        abort(400, description="La categoría especificada no existe")
    
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "completed": completed,
        "category_id": category_id
    }
    
    tasks.append(new_task)
    save_data()
    return jsonify(new_task), 201

#CREAR UNA CATEGORIA:
@app.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    name = data.get("name", "").strip()

    # Validaciones
    if not name:
        abort(400, description="El nombre de la categoría no puede estar vacío")
    
    if any(c["name"].lower() == name.lower() for c in categories):
        abort(400, description="La categoría ya existe")
    
    new_category = {
        "id": len(categories) + 1,
        "name": name
    }
    
    categories.append(new_category)
    save_data()
    return jsonify(new_category), 201

#ELIMINAR UNA TAREA:
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        abort(404, description="Tarea no encontrada")
    
    tasks.remove(task)
    save_data()
    return jsonify({"message": "Tarea eliminada"}), 200

#ELIMINAR UNA CATEGORIA:
@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = next((category for category in categories if category["id"] == category_id), None)
    if category is None:
        abort(404, description="Categoría no encontrada")
    
    # Verificar si la categoría tiene tareas asociadas
    if any(task["category_id"] == category_id for task in tasks):
        abort(400, description="No se puede eliminar la categoría porque tiene tareas asociadas")
    
    categories.remove(category)
    save_data()
    return jsonify({"message": "Categoría eliminada"}), 200

#FILTRAR POR TAREA COMPLETADA:
@app.route('/tasks', methods=['GET'])
def get_filtered_tasks():
    completed = request.args.get('completed', type=str)
    
    if completed is not None:
        if completed.lower() == "true":
            filtered_tasks = [task for task in tasks if task["completed"]]
        elif completed.lower() == "false":
            filtered_tasks = [task for task in tasks if not task["completed"]]
        else:
            abort(400, description="El valor de 'completed' debe ser 'true' o 'false'")
    else:
        filtered_tasks = tasks
    
    return jsonify(filtered_tasks)


#OBTENER TODAS LAS TAREAS DE UNA CATEGORIA:
@app.route('/categories/<int:category_id>/tasks', methods=['GET'])
def get_category_tasks(category_id):
    category = next((category for category in categories if category["id"] == category_id), None)
    if category is None:
        abort(404, description="Categoría no encontrada")
    
    category_tasks = [task for task in tasks if task["category_id"] == category_id]
    return jsonify(category_tasks)

#ACTUALIZACIÓN COMPLETA DE UNA CATEGORIA:
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        abort(404, description="Tarea no encontrada")
    
    data = request.json
    title = data.get("title", "").strip()
    category_id = data.get("category_id")
    completed = data.get("completed")

    # Validaciones
    if not title or not (3 <= len(title) <= 100):
        abort(400, description="El título debe tener entre 3 y 100 caracteres")
    
    if any(t["title"].lower() == title.lower() and t["category_id"] == category_id for t in tasks):
        abort(400, description="El título ya existe en esta categoría")
    
    if not isinstance(completed, bool):
        abort(400, description="El campo 'completed' debe ser un booleano")
    
    if not any(c["id"] == category_id for c in categories):
        abort(400, description="La categoría especificada no existe")
    
    task["title"] = title
    task["completed"] = completed
    task["category_id"] = category_id

    save_data()
    return jsonify(task)


if __name__ == '__main__':
    app.run(debug=True)