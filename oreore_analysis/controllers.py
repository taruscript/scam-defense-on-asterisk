from flask import Flask, render_template, Blueprint
from apps import scam_check

app = Flask(__name__)

# ★分割先のコントローラー(Blueprint)を登録
# app.register_blueprint(transcription.app)
app.register_blueprint(scam_check.app)