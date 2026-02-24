from flask import Flask, render_template, request, send_file
import pandas as pd
from fito import calcular_fito

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return "Nenhum arquivo enviado"

    file = request.files["file"]

    if file.filename == "":
        return "Arquivo inválido"

    try:
        df = pd.read_excel(file)
    except Exception as e:
        return f"Erro ao ler Excel: {e}"

    if not {"spp", "parc", "dap"}.issubset(df.columns):
        return "O Excel precisa ter colunas: spp, parc, dap"

    try:
        resultado = calcular_fito(df, 1000)
    except Exception as e:
        return f"Erro no cálculo: {e}"

    resultado.to_csv("resultado.csv", sep=";", decimal=",", encoding="utf-8")

    return send_file("resultado.csv", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)