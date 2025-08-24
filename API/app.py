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

# funcion para un codigo mas limpio
def boards_to_dict(board):
    return {
        "id": board.id,
        "titulo": board.titulo,
        "short_name": board.short_name,
        "descripcion": board.descripcion,
        "portada": board.portada,
        "featured": board.featured,
    }

# Metodo GET
@app.route("/api/boards")
def get_boards():
    boards = Board.objects.all()
    data = [boards_to_dict(b) for b in boards]
    return jsonify(data)

# Metodo POST
@app.route("api/boards")
def post_boards():
    try:
        data = request.get_json()

        if not data or 'titulo' not in data:
            return jsonify({"error": "Titulo requerido"})
        
        board = Board.objects.create(
            titulo = data["titulo"],
            contenido = data["contenido"],
            portada = data["portada"],
            featured = data.get["featured"],
        )
        return jsonify({"mensaje": "Board creado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
