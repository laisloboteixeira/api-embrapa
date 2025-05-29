
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extrair_tabela(nome, ano='2023'):
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"

    config = {
        "producao": {"opcao": "opt_02"},
        "processamento_viniferas": {"opcao": "opt_03"},
        "processamento_americanas": {"subopcao": "subopt_02", "opcao": "opt_03"},
        "processamento_mesa": {"subopcao": "subopt_03", "opcao": "opt_03"},
        "processamento_semclass": {"subopcao": "subopt_04", "opcao": "opt_03"},
        "comercializacao": {"opcao": "opt_04"},
        "importacao_vinhos": {"subopcao": "subopt_01", "opcao": "opt_05"},
        "importacao_espumantes": {"subopcao": "subopt_02", "opcao": "opt_05"},
        "importacao_frescas": {"subopcao": "subopt_03", "opcao": "opt_05"},
        "importacao_passas": {"subopcao": "subopt_04", "opcao": "opt_05"},
        "importacao_suco": {"subopcao": "subopt_04", "opcao": "opt_05"},
        "exportacao_vinhos": {"opcao": "opt_06"},
        "exportacao_espumantes": {"subopcao": "subopt_02", "opcao": "opt_06"},
        "exportacao_frescas": {"subopcao": "subopt_03", "opcao": "opt_06"},
        "exportacao_suco": {"subopcao": "subopt_04", "opcao": "opt_06"}
    }

    if nome not in config:
        return None, f"Tipo inválido: {nome}"

    params = {"ano": ano, **config[nome]}

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")
        if not tables:
            return None, "Nenhuma tabela encontrada"

        melhor_df = None
        maior_score = 0
        for t in tables:
            try:
                df = pd.read_html(str(t), decimal=",", thousands=".")[0]
                if df.shape[1] < 2 or df.shape[0] < 2:
                    continue
                score = df.shape[0] * df.shape[1]
                if score > maior_score:
                    melhor_df = df
                    maior_score = score
            except:
                continue

        if melhor_df is not None:
            melhor_df = melhor_df.dropna(axis=1, how='all')
            melhor_df = melhor_df[~melhor_df.apply(
                lambda row: any(
                    isinstance(val, str) and (
                        "Fonte" in val or "Elaboração" in val or len(val) > 300
                    ) for val in row
                ), axis=1)]

            for col in melhor_df.columns:
                if melhor_df[col].dtype in ['int64', 'float64'] or melhor_df[col].apply(lambda x: str(x).isdigit()).any():
                    melhor_df[col] = melhor_df[col].apply(
                        lambda x: f'{int(x):,}'.replace(",", ".") if pd.notnull(x) and str(x).replace(".", "").isdigit() else x
                    )

            return melhor_df.to_dict(orient="records"), None

        return None, "Nenhuma tabela válida encontrada"
    except Exception as e:
        return None, str(e)
