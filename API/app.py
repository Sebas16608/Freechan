from flask import Flask, jsonify, request
import django
import sys
import os
from flask_cors import CORS

# Configuracion de rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, '..')
sys.path.append(backend_path)

# configuracion de django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foro.settings")
django.setup()

app = Flask(__name__)
CORS(app)

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

# Metodo GET (todos los boards)
@app.route("/api/boards", methods=["GET"])
def get_boards():
    boards = Board.objects.all()
    data = [boards_to_dict(b) for b in boards]
    return jsonify(data), 200

# 🔥 NUEVO: Metodo GET para un board específico
@app.route("/api/boards/<int:id>", methods=["GET"])
def get_board(id):
    try:
        board = Board.objects.get(id=id)
        return jsonify(boards_to_dict(board)), 200
    except Board.DoesNotExist:
        return jsonify({"error": "Board no existente"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
            portada=None,
            featured=data.get("featured", False)
        )
        return jsonify({"mensaje": "Board creado correctamente", "board": boards_to_dict(board)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Metodo PUT
@app.route("/api/boards/<int:id>", methods=["PUT"])
def update_board(id):
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

# Metodo DELETE
@app.route("/api/boards/<int:id>", methods=["DELETE"])
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
API Threads
"""
from threads.models import Thread

# funcion para convertir un thread a dict
def threads_to_dict(thread):
    return {
        "id": thread.id,
        "titulo": thread.titulo,
        "contenido": thread.contenido,
        "imagen": thread.imagen.url if thread.imagen else None,
        "created": thread.created,
        "featured": thread.featured,
        "board_id": thread.board.id if thread.board else None, 
    }

# Metodo GET (todos los threads)
@app.route("/api/threads", methods=["GET"])
def get_threads():
    threads = Thread.objects.all()
    data = [threads_to_dict(t) for t in threads]
    return jsonify(data), 200

# 🔥 NUEVO: Metodo GET para un thread específico
@app.route("/api/threads/<int:id>", methods=["GET"])
def get_thread(id):
    try:
        thread = Thread.objects.get(id=id)
        return jsonify(threads_to_dict(thread)), 200
    except Thread.DoesNotExist:
        return jsonify({"error": "Thread no existente"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Metodo POST
@app.route("/api/threads", methods=["POST"])
def post_threads():
    try:
        data = request.get_json()
        if not data or "titulo" not in data:
            return jsonify({"error": "Titulo requerido"}), 400
        thread = Thread.objects.create(
            titulo=data["titulo"],
            contenido=data["contenido"],
            imagen=data.get("imagen"),
            board_id=data["board_id"],
            created=data.get("created"),
            featured=data.get("featured", False)
        )
        return jsonify({"mensaje": "Thread creado correctamente", "thread": threads_to_dict(thread)}), 201
    except Exception as e:
        return jsonify({"error": str(e)})

# Metodo PUT
@app.route("/api/threads/<int:id>", methods=["PUT"])
def update_thread(id):
    try:
        thread = Thread.objects.get(id=id)
        data = request.get_json()

        if "titulo" in data:
            thread.titulo = data["titulo"]
        if "contenido" in data:
            thread.contenido = data["contenido"]
        if "imagen" in data:
            thread.imagen = data["imagen"]
        return jsonify({"mensaje": f"El thread con el id: {id} se ha modificado correctamente"}), 200
    except Thread.DoesNotExist:
        return jsonify({"error": "El thread no existe"}), 400
    except Exception as e:
        return jsonify({"error": str(e)})

# Metodo DELETE
@app.route("/api/threads/<int:id>", methods=["DELETE"])
def delete_thread(id):
    try:
        thread = Thread.objects.get(id=id)
        thread.delete()
        return jsonify({"mensaje": f"El thread con el id {id} fue eliminado correctamente"})
    except Thread.DoesNotExist:
        return jsonify({"error": "El thread no existe"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

"""
API Posts
"""
from posts.models import Post

# funcion para codigo mas limpio
def post_to_dict(post):
    return {
        "id": post.id,
        "contenido": post.contenido,
        "imagen": post.imagen.url if post.imagen else None,
        "created": post.created,
        "featured": post.featured,
        "thread_id": post.thread.id if post.thread else None,
    }

# Metodo GET (todos los posts)
@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = Post.objects.all()
    data = [post_to_dict(p) for p in posts]
    return jsonify(data), 200

# 🔥 NUEVO: Metodo GET para un post específico
@app.route("/api/posts/<int:id>", methods=["GET"])
def get_post(id):
    try:
        post = Post.objects.get(id=id)
        return jsonify(post_to_dict(post)), 200
    except Post.DoesNotExist:
        return jsonify({"error": "Post no existente"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Metodo POST
@app.route("/api/posts", methods=["POST"])
def post_posts():
    try:
        data = request.get_json()
        if not data or "contenido" not in data:
            return jsonify({"error": "Contenido requerido"}), 400
        posts = Post.objects.create(
            contenido=data["contenido"],
            imagen=data.get("imagen"),
            created=data.get("created"),
            featured=data.get("featured"),
            thread_id=data["thread_id"],
        )
        return jsonify({"mensaje": "Post creado", "post": post_to_dict(posts)}), 201
    except Exception as e:
        return jsonify({"error": str(e)})

# Metodo PUT
@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_posts(id):
    try:
        posts = Post.objects.get(id=id)
        data = request.get_json()
        if "contenido" in data:
            posts.contenido = data["contenido"]
        if "imagen" in data:
            posts.imagen = data["imagen"]
        return jsonify({"mensaje": f"El post con el id {id} fue actualizado correctamente"})
    except Post.DoesNotExist:
        return jsonify({"error": "El Post no existe"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# Metodo Delete
@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    try:
        posts = Post.objects.get(id=id)
        posts.delete()
        return jsonify({"mensaje": f"El post con el id {id} se elimino correctamente"})
    except Post.DoesNotExist:
        return jsonify({"error": "El post no existe"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=1900)