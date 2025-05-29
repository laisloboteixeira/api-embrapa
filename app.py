
from flask import Flask, jsonify, render_template, request
from embrapa_scraper import extrair_tabela

app = Flask(__name__)

ROTAS_VISUAIS = {
    "Producao": "/producao",
    "Comercializacao": "/comercializacao",
    "Processamento Viniferas": "/processamento_viniferas",
    "Processamento Americanas e Hibridas": "/processamento_americanas",
    "Processamento Mesa": "/processamento_mesa",
    "Processamento Semclass": "/processamento_semclass",
    "Importacao Vinhos de Mesa": "/importacao_vinhos",
    "Importacao Espumantes": "/importacao_espumantes",
    "Importacao Frescas": "/importacao_frescas",
    "Importacao Passas": "/importacao_passas",
    "Importacao Suco": "/importacao_suco",
    "Exportacao Vinhos de Mesa": "/exportacao_vinhos",
    "Exportacao Espumantes": "/exportacao_espumantes",
    "Exportacao Frescas": "/exportacao_frescas",
    "Exportacao Suco": "/exportacao_suco"
}

def formatar_titulo(texto):
    palavras = texto.replace("_", " ").split()
    preposicoes = {"de", "da", "do", "das", "dos", "e", "em", "para", "por", "com", "sem"}
    return " ".join([
        palavra.capitalize() if palavra.lower() not in preposicoes else palavra.lower()
        for palavra in palavras
    ])

@app.route("/")
def home():
    return render_template("index.html", rotas=ROTAS_VISUAIS)

@app.route("/api/<tipo>")
def api(tipo):
    ano = request.args.get("ano", "2023")
    dados, erro = extrair_tabela(tipo, ano)
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(dados)

@app.route("/<tipo>")
def visual(tipo):
    ano = request.args.get("ano", "2023")
    dados, erro = extrair_tabela(tipo, ano)

    TITULOS = {
        "producao": "Produção",
        "comercializacao": "Comercialização",
        "processamento_viniferas": "Processamento - Viníferas",
        "processamento_americanas": "Processamento - Americanas e Híbridas",
        "processamento_mesa": "Processamento - Uvas de Mesa",
        "processamento_semclass": "Processamento - Sem Classificação",
        "importacao_vinhos": "Importação - Vinhos de Mesa",
        "importacao_espumantes": "Importação - Espumantes",
        "importacao_frescas": "Importação - Uvas Frescas",
        "importacao_passas": "Importação - Uvas Passas",
        "importacao_suco": "Importação - Suco de Uva",
        "exportacao_vinhos": "Exportação - Vinhos de Mesa",
        "exportacao_espumantes": "Exportação - Espumantes",
        "exportacao_frescas": "Exportação - Uvas Frescas",
        "exportacao_suco": "Exportação - Suco de Uva"
    }

    titulo = TITULOS.get(tipo, formatar_titulo(tipo))
    return render_template("tabela.html", tabela=dados if not erro else None, titulo=titulo, tipo=tipo, ano=ano)

if __name__ == "__main__":
    app.run(debug=True)
