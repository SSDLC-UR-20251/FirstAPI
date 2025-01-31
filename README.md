# API de Gestión de Tareas

Este ejercicio consiste en la creación y mejora de una API para la gestión de tareas categorizadas. Se proporcionan algunos endpoints básicos. Deberán implementar nuevas funcionalidades para completar el ejercicio.

## **Endpoints Proporcionados**

### **1. Obtener todas las categorías**

**GET /categories**

- Retorna una lista de todas las categorías disponibles.

**Ejemplo de respuesta:**

```json
[
    {"id": 1, "name": "Trabajo"},
    {"id": 2, "name": "Estudio"}
]
```

---
### **2. Obtener todas las tareas**

**GET /tasks**

- Retorna una lista de todas las tareas sin filtros ni paginación.

**Ejemplo de respuesta:**

```json
[
    {"id": 1, "title": "Leer documentación", "completed": false, "category_id": 2},
    {"id": 2, "title": "Revisar código", "completed": true, "category_id": 1}
]
```

---
### **3. Actualización parcial de una tarea**

**PATCH /tasks/{task_id}**

- Permite modificar parcialmente una tarea enviando solo los campos a actualizar.

**Ejemplo de solicitud:**

```json
{
    "completed": true
}
```

**Ejemplo de respuesta:**

```json
{
    "id": 1, "title": "Leer documentación", "completed": true, "category_id": 2
}
```

---
## **Ejercicios a Implementar**

### **1. Validaciones y manejo de errores**

Se deben implementar las siguientes validaciones y manejo de errores en los endpoints:

#### **Validaciones generales:**
- **Título de la tarea:** Debe tener entre 3 y 100 caracteres.
- **Duplicación de título:** No se debe permitir que una tarea tenga el mismo título dentro de una categoría.
- **Estado de tarea:** El campo `completed` debe ser un booleano (`true` o `false`).
- **Categoría de la tarea:** `category_id` debe existir en la lista de categorías.
- **Nombre de la categoría:** No debe estar vacío y no debe repetirse.

#### **Manejo de errores:**
- **400 Bad Request**:
  - Si falta un campo obligatorio (`title`, `category_id`, `name`).
  - Si el título de la tarea no cumple con la longitud mínima/máxima.
  - Si `category_id` no existe al crear/actualizar una tarea.
  - Si el título de la tarea ya existe en la misma categoría.
  - Si se intenta eliminar una categoría con tareas asociadas.
- **404 Not Found**:
  - Si la tarea o categoría no existe al intentar acceder, actualizar o eliminar.

Estas validaciones deben aplicarse a los siguientes endpoints:
- **Creación de tarea (`POST /tasks`)**
- **Creación de categoría (`POST /categories`)**
- **Actualización completa de una tarea (`PUT /tasks/{task_id}`)**
- **Actualización completa de una categoría (`PUT /categories/{category_id}`)**
- **Eliminación de tarea (`DELETE /tasks/{task_id}`)**
- **Eliminación de categoría (`DELETE /categories/{category_id}`)**

### **2. Filtrar tareas completadas**

**GET /tasks?completed=true**

- Implementar un filtro que permita obtener solo las tareas que han sido completadas.
- **Ejemplo de solicitud:** `GET /tasks?completed=true`

### **3. Obtener todas las tareas de una categoría**

**GET /categories/{category_id}/tasks**

- Retorna todas las tareas pertenecientes a una categoría específica.
- **Ejemplo de solicitud:** `GET /categories/2/tasks`

### **4. Eliminar una tarea**

**DELETE /tasks/{task_id}**

- Permite eliminar una tarea específica.
- **Ejemplo de solicitud:** `DELETE /tasks/1`

### **5. Eliminar una categoría**

**DELETE /categories/{category_id}**

- Permite eliminar una categoría solo si no tiene tareas asociadas.
- **Ejemplo de solicitud:** `DELETE /categories/2`

### **6. Crear una nueva tarea**

**POST /tasks**

- Permite la creación de una nueva tarea.
- **Ejemplo de solicitud:**

```json
{
    "id": 5,
    "title": "Preparar presentación de seguridad",
    "completed": false,
    "category_id": 1
}
```

### **7. Crear una nueva categoría**

**POST /categories**

- Permite la creación de una nueva categoría.
- **Ejemplo de solicitud:**

```json
{
    "id": 3,
    "name": "Personal"
}
```

### **8. Actualizar completamente una tarea**

**PUT /tasks/{task_id}**

- Permite actualizar completamente una tarea existente.
- **Ejemplo de solicitud:**

```json
{
    "id": 1,
    "title": "Preparar presentación de seguridad",
    "completed": true,
    "category_id": 1
}
```

### **9. Actualizar completamente una categoría**

**PUT /categories/{category_id}**

- Permite actualizar completamente una categoría existente.
- **Ejemplo de solicitud:**

```json
{
    "id": 3,
    "name": "Personal"
}
```
---
### **Entrega del Ejercicio**

Deberan seguir los siguientes pasos para clonar y entregar el ejercicio:

1. Clonar el repositorio base

Ejecutar el siguiente comando en la terminal:

`git clone <https://github.com/SSDLC-UR-20251/FirstAPI.git>`

`cd FirstAPI`

Asegurar que estan usando localmente el usuario y el correo con el que quedaron registrados: 

`git config --global user.name "your_name"`

`git config --global user.email "your_email"`

2. Crear una nueva rama de desarrollo

Cada estudiante debe crear una rama siguiendo el formato feature/<nombre_completo>:

`git checkout -b feature/<nombre_completo>`

3. Implementar los cambios

Realizar los cambios necesarios en el código y probar los endpoints.

4. Guardar y confirmar los cambios

`git add .`

`git commit -m "Implementación de endpoints y validaciones"`

5. Subir la rama al repositorio remoto

`git push origin feature/<nombre_completo>`

