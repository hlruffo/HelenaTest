import streamlit as st
import openai
from dotenv import load_dotenv
import os
import json

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave API da OpenAI do arquivo .env
openai.api_key = os.getenv('OPENAI_API_KEY')

# Carregar as instruções do assistente de um arquivo JSON
with open('instrucoes.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    instructions = config["instructions"]

# Função para enviar mensagens ao assistente
def enviar_mensagem_ao_assistente(mensagem):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Modelo correto
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": mensagem}
        ]
    )
    return response['choices'][0]['message']['content']

# Interface de chat com Streamlit
st.title("Chat com Assistente LigoSIM_Helena")

# Histórico da conversa
if 'historico' not in st.session_state:
    st.session_state.historico = []

# Caixa de entrada para a mensagem do usuário
mensagem_usuario = st.text_input("Digite sua mensagem:")

# Enviar mensagem
if st.button("Enviar"):
    if mensagem_usuario:
        # Adicionar mensagem do usuário ao histórico
        st.session_state.historico.append({"role": "user", "content": mensagem_usuario})
        
        # Obter resposta do assistente
        resposta_assistente = enviar_mensagem_ao_assistente(mensagem_usuario)
        
        # Adicionar resposta do assistente ao histórico
        st.session_state.historico.append({"role": "assistant", "content": resposta_assistente})

# Exibir o histórico de mensagens
for chat in st.session_state.historico:
    if chat['role'] == 'user':
        st.write(f"Você: {chat['content']}")
    else:
        st.write(f"Assistente Helena: {chat['content']}")
