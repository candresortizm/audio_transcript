import os
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from dotenv import load_dotenv
from mangum import Mangum
import json
from app.audio_analysis import get_sentiment_analysis, obtener_analisis, obtener_desde_json

load_dotenv() 

app = Flask(__name__)

handler = Mangum(app)  # Entry point for AWS Lambda.

@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

@app.route("/leer_json", methods=["GET"])
def leer_json():
    resultado_json, transcripcion_completa = obtener_desde_json()
    return render_template("resultado.html", jsonfile=json.dumps(resultado_json), transcripcionCompleta = transcripcion_completa)

@app.route("/analisis", methods=["POST"])
def analisis():
    file = request.files.get("audio")
    if not file or file.filename == "":
        flash("Por favor escoge primero un archivo de audio")
        return redirect(url_for("index"))
    resultado_json, transcripcion_completa = obtener_analisis(file)

    return render_template("resultado.html", jsonfile = json.dumps(resultado_json), transcripcionCompleta = transcripcion_completa)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)