from google import genai
import os

# olhando os modelos disponíveis para a API utilizada
try:
    client = genai.Client()
    models = client.models.list()
    for model in models:
        print(f"Modelo: {model.name}")
except Exception as e:
    print(f"Erro ao listar modelos: {e}")
