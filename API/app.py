from flask import Flask, jsonify, request
import django
import sys
import os

# Configuracion de rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, '..')
sys.path.append(backend_path)

# configuracion de django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foro.settings")
django.setup()

app = Flask(__name__)

# Boards' API
from boards.models import Board

# función para convertir un Board a dict
def boards_to_dict(board):
    return {
        "id": board.id,
        "titulo": board.titulo,
        "short_name": board.short_name,
        "descripcion": board.descripcion,
        "portada": board.portada.url if board.portada else None,
        "featured": board.featured,
    }

# Metodo GET
@app.route("/api/boards", methods=["GET"])
def get_boards():
    boards = Board.objects.all()
    data = [boards_to_dict(b) for b in boards]
    return jsonify(data), 200

# Metodo POST
@app.route("/api/boards", methods=["POST"])
def post_boards():
    try:
        data = request.get_json()
        if not data or "titulo" not in data:
            return jsonify({"error": "Titulo requerido"}), 400

        board = Board.objects.create(
            titulo=data["titulo"],
            short_name=data.get("short_name", "BN"),
            descripcion=data.get("descripcion", ""),
            portada=None,  # Subida de imagen puedes manejarlo aparte
            featured=data.get("featured", False)
        )
        return jsonify({"mensaje": "Board creado correctamente", "board": boards_to_dict(board)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Metodo PUT
@app.route("/api/boards/<int:id>", methods=["PUT"])
def update_boards(id):
    try:
        board = Board.objects.get(id=id)
        data = request.get_json()

        if "titulo" in data:
            board.titulo = data["titulo"]
        if "short_name" in data:
            board.short_name = data["short_name"]
        if "descripcion" in data:
            board.descripcion = data["descripcion"]
        if "featured" in data:
            board.featured = data["featured"]

        board.save()
        return jsonify({"mensaje": "Board actualizado correctamente", "board": boards_to_dict(board)}), 200
    except Board.DoesNotExist:
        return jsonify({"error": "Board no existente"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Metodo DELET
@app.route("/api/boards/<int:id>", methods=["DELET"])
def delete_board(id):
    try:
        board = Board.objects.get(id=id)
        board.delete()
        return jsonify({"mensaje": f"El board con el id: {id} fue eliminado correctamente"})
    except Board.DoesNotExist:
        return jsonify({"error": "El board no existe"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
"""
API de Threads
"""
from threads.models import Thread

# funcion para conevertir un thread a dict
def thread_to_dict(thread):
    return {
        "id": thread.id,
        "titulo": thread.titulo,
        "contenido": thread.contenido,
        "imagen": thread.imagen.url if thread.imagen else None,
        "created": thread.created,
        "featured": thread.featured,
    }

# Metodo GET
@app.route("/api/threads", methods=["GET"])
def get_thread():
    thread = Thread.objects.all()
    data=[thread_to_dict(t) for t in thread]
    return jsonify(data), 200



if __name__ == "__main__":
    app.run(debug=True)
