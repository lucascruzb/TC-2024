import json
import re

def criar_registradores_estados(data):
    """
    Função que processa os dados do JSON e retorna registradores e estados.
    """
    registradores = ""
    estados = ""

    registers = data.get("registers")
    states = data.get("states")

    if not registers or not states:
        return "ERRO Dados de registradores ou estados ausentes.", ""

    # Processar registradores
    registradores_str = ", ".join(f"{reg}={valor}" for reg, valor in registers.items())
    registradores_str = registradores_str.replace(" ", "")

    # Processar estados
    estados_str = "\n".join(states)

    contudoDoJson = f"{registradores_str}\n{estados_str}"

    primeiraLinha = True
    linhas = contudoDoJson.splitlines()

    for linha in linhas:
        linha = linha.strip()  # Remove quebras de linha e espaços extras
        if primeiraLinha:
            padraoCorretoRegistradores = r'^([a-z]=\d+)(,[a-z]=\d+)*$'

            # Verifica se a linha corresponde ao padrão
            if re.fullmatch(padraoCorretoRegistradores, linha, re.IGNORECASE):
                registradores = linha + "\n"
            else:
                return "ERRO A primeira linha não está no formato esperado.", " "

        else:
            padraoCorretoEstados = r"^[\+\-][a-zA-Z](,\d+)*(,?#)?$"
            if re.fullmatch(padraoCorretoEstados, linha, re.IGNORECASE):
                estados = estados + linha + "\n"
            else:
                return "ERRO Descrição de estado incorreto", " "

        primeiraLinha = False

    return registradores, estados

class AbrirArquivo:
    def abrir(caminho_arquivo):
        """
        Abre um arquivo JSON, lê os dados e valida registradores e estados.
        """
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                data = json.load(arquivo)
                return criar_registradores_estados(data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return f"ERRO ao abrir o arquivo: {str(e)}", ""

    def abrir_do_terminal(arquivo_json):
        """
        Recebe dados JSON diretamente de uma variável (ex.: frontend) e processa os registradores e estados.
        """
        try:
            data = json.loads(arquivo_json)
            return criar_registradores_estados(data)
        except json.JSONDecodeError as e:
            return f"ERRO ao processar o JSON: {str(e)}", ""
