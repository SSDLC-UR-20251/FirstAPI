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

def validar_titulo_tarea(title):
    if len(title) < 3 or len(title) > 100:
        abort(400, description="El título de la tarea debe tener entre 3 y 100 caracteres")


def validar_titulo_duplicado(id,title):
    for task in tasks:
        if task["category_id"] == id and task["title"] == title :
            abort(400, description="El título de la tarea ya existe en esta categoría")

def bool_estado_tarea(status):
    if not isinstance(status, bool):
        abort(400, description="El campo 'completed' debe ser un valor booleano")

def task_category(category_id):
    for category in categories:
        if not any(category["id"] == category_id):
            abort(400,description="El category_id no existe")

def category_name(name):
    for category in categories:
        if not name or any(category["name"] == name): 
            abort(400, description="El nombre de la categoría no debe estar vacío o repetirse")

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    validar_titulo_tarea(data["title"])
    bool_estado_tarea(data["completed"])
    #task_category(data["category_id"])
    
    new_task={
        "id" : len(tasks) + 1,
        "title" : data["title"],
        "completed" : data.get("completed",False),
        "category_id" :  data["category_id"]
    }
    validar_titulo_duplicado(data["category_id"],data["title"])
    tasks.append(new_task)
    save_data()
    return jsonify(new_task), 201

@app.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    category_name(data['name'])
    new_category = {"id": len(categories)+1,
                    "name": data['name']
                     }
    categories.append(new_category)
    save_data()
    return jsonify(new_category), 201

if __name__ == '__main__':
    app.run(debug=True)
