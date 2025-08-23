from flask import Flask, jsonify
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freechan.settings")
django.setup()

from boards.models import Board

app = Flask(__name__)

@app.route("/api/boards")
def get_boards():
    boards = Board.objects.all()
