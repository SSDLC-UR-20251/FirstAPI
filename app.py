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

#IMPLEMENTACIONES LABORATORIO
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    validate_task (data['title'])
    if not request.json or not 'title' in request.json:
        abort(400,"aaaaaa")
    if not validate_task(request.json['title']):
        abort(400, description="El titulo debe tener entre 3 y 100 caracteres")
    task = {
        'id': len(tasks) + 1,
        'title': request.json['title'],
        #'descripcion': request.json.get('descripcion', ""),
        #'categoria': request.json.get('categoria', "")
    }
    tasks.append(task)
    save_data()
    return jsonify(task), 201

def validate_task(titulo):
    if ( len(titulo) > 3 and len(titulo)< 100):
        return True

@app.route('/tasks/completed', methods=['GET'])
def get_tasks_completed():
    return jsonify([task for task in tasks if task.get('completed', True)])

@app.route('/categories/f"{id}"', methods=['GET'])
def filterCategories():
    return jsonify([task for task in categories if task.get("category_id", True)])

if __name__ == '__main__':
    app.run(debug=True)
