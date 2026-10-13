import os

import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)


def conectar():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


def crear_tabla(cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS tareas ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "titulo VARCHAR(100) NOT NULL, "
        "completada BOOLEAN DEFAULT FALSE)"
    )


@app.get("/api/tareas")
def listar():
    conexion = conectar()
    with conexion.cursor() as cursor:
        crear_tabla(cursor)
        cursor.execute("SELECT id, titulo, completada FROM tareas")
        tareas = cursor.fetchall()
    conexion.close()
    return jsonify(tareas)


@app.post("/api/tareas")
def crear():
    titulo = (request.get_json() or {}).get("titulo", "").strip()
    if not titulo:
        return jsonify(error="El título es obligatorio"), 400
    conexion = conectar()
    with conexion.cursor() as cursor:
        crear_tabla(cursor)
        cursor.execute("INSERT INTO tareas (titulo) VALUES (%s)", (titulo,))
        nuevo_id = cursor.lastrowid
    conexion.close()
    return jsonify(id=nuevo_id, titulo=titulo, completada=False), 201


@app.put("/api/tareas/<int:tarea_id>")
def alternar(tarea_id):
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE tareas SET completada = NOT completada WHERE id = %s",
            (tarea_id,),
        )
    conexion.close()
    return jsonify(id=tarea_id)


@app.delete("/api/tareas/<int:tarea_id>")
def eliminar(tarea_id):
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
    conexion.close()
    return jsonify(eliminada=tarea_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
