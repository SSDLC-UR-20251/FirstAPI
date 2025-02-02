
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

#EJERCICIO 2: Filtrar tareas completadas
@app.route('/completasks', methods=['GET'])
def get_completasks():
    list = []
    for i in tasks:
        if i['completed'] == True:
            list.append(i)
    return jsonify(list)

#EJERCICIO 3: Obtener todaas las tareas de una categoria
@app.route('/catasks/<int:categor_id>', methods=['GET'])
def get_catasks(categor_id):
    list =[]
    for i in tasks:
        if i['category_id'] == categor_id:
            list.append(i)
    return jsonify(list)

#EJERCICIO 4: Eliminar una tarea
@app.route('/deltask/<int:id>', methods=['DELETE'])
def del_deltask(id):
    cont = -1
    for i in tasks:
        cont += 1
        if i['id'] == id:
            tasks.pop(cont)
    return jsonify(tasks)

#EJERCICIO 5: Eliminar una categoria
@app.route('/delcat/<int:cat_id>', methods=['DELETE'])
def del_delcat(cat_id):
    cont = -1
    cont2 = -1
    for i in tasks:
        cont += 1
        if i['category_id'] == cat_id:
            tasks.pop(cont)
    for i in categories:
        cont2 += 1
        if i['id'] == cat_id:
            categories.pop(cont2)
    return jsonify(categories)

#EJERCICIO 6: Crear una nueva tarea
@app.route('/newtask', methods=['POST'])
def newtask():
    data = request.json
    tasks.append(data)
    return jsonify(data)

#EJERCICIO 7: Crear una nueva categoria
@app.route('/newcat', methods=['POST'])
def newcat():
    data = request.json
    categories.append(data)
    return jsonify(data)

#EJERCICIO 8: Actualizar completamente una tarea
@app.route('/actask/<int:task_id>', methods=['PUT'])
def actask(task_id):
    cont = -1
    data = request.json
    list = ['title','completed','category_id']
    for i in tasks:
        cont +=1
        if i['id'] == task_id:
            for j in list:
                tasks[cont][j] = data[j]
    return jsonify(data)

#EJERCICIO 9: Actualizar una categoria
@app.route('/actcateg/<int:id>', methods=['PUT'])
def actcateg(id):
    cont = -1
    data = request.json
    list = ['name']
    for i in categories:
        cont +=1
        if i['id'] == id:
            for j in list:
                categories[cont][j] = data[j]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
