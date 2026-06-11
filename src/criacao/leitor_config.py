import json

class LeitorConfig:
    @staticmethod
    def ler(caminho_arquivo: str) -> dict:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
