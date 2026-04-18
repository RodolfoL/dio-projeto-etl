import csv
from http import client
import json
from openai import OpenAI

client = OpenAI(
  api_key="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"
)

def extrair_dados(arquivo_csv):
    dados = []
    with open(arquivo_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dados.append({
                'ID': row.get('ID'),
                'NOME': row.get('NOME'),
                'CARTÃO': row.get('CARTÃO'),
                'CONTA': row.get('CONTA')
            })
    return dados

def gerar_mensagem_ia(user):
    completion = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system", 
                "content": "Você é um especialista em markting bancário."
            },
            {"role": "user", 
             "content": f"Crie uma mensagem personalizada para o cliente {user['NOME']} falando sobre a importancia de investir. (máximo de 100 caracteres)"
            }
        ]
    )
    return completion.choices[0].message.content

def carregar_usuario_json(usuario, mensagem):
    usuario['MENSAGEM'] = mensagem
    try:
        with open("dados.json", 'r', encoding='utf-8') as file:
            dados = json.load(file)
    except FileNotFoundError:
        dados = {}
    dados.update({usuario['ID']: usuario})
    with open("dados.json", 'w', encoding='utf-8') as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)

usuarios = extrair_dados('usuarios.csv')
for usuario in usuarios:
        mensagem = gerar_mensagem_ia(usuario)
        usuario['MENSAGEM'] = []
        usuario['MENSAGEM'].append({mensagem})
        carregar_usuario_json(usuario, mensagem) 
        print(f"Mensagem para {usuario['NOME']}: {mensagem}")

