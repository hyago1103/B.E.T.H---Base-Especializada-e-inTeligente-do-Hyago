import streamlit as st
import google.generativeai as genai
import time

# --- Configuração do app ---
st.set_page_config(
    page_title="B.E.T.H - Base Especializada e inTeligente do Hyago",
    page_icon="",
    layout="wide"
)

# --- Configuração segura da API ---
genai.configure(st.write(st.secrets)["GOOGLE_API_KEY"])
modelo = genai.GenerativeModel("gemini-2.5-pro")

# --- Barra lateral ---
st.sidebar.title("💬 Histórico de Chats")
if "historico_chats" not in st.session_state:
    st.session_state["historico_chats"] = {"Chat 1": []}
if "chat_atual" not in st.session_state:
    st.session_state.chat_atual = "Chat 1"

# Botão de novo chat
if st.sidebar.button("➕ Novo Chat"):
    novo_nome = f"Chat {len(st.session_state['historico_chats']) + 1}"
    st.session_state["historico_chats"][novo_nome] = []
    st.session_state.chat_atual = novo_nome
    st.session_state["lista_mensagens"] = []

# Selecionar chat existente
chat_selecionado = st.sidebar.radio(
    "Conversas",
    options=list(st.session_state["historico_chats"].keys()),
    index=list(st.session_state["historico_chats"].keys()).index(st.session_state.chat_atual)
)
st.session_state.chat_atual = chat_selecionado

# Botão de limpar chat atual
if st.sidebar.button("🗑 Limpar chat"):
    st.session_state["lista_mensagens"] = []
    st.session_state["historico_chats"][st.session_state.chat_atual] = []

# --- Conteúdo principal ---
st.title(f"🤖 {st.session_state.chat_atual}")

# Carrega histórico do chat atual
if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = st.session_state["historico_chats"][st.session_state.chat_atual]

# Exibe histórico com cores diferentes
for msg in st.session_state["lista_mensagens"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(f"**Você:** {msg['content']}")
    else:
        st.chat_message("assistant").markdown(f"**B.E.T.H:** {msg['content']}")

# Input do usuário
mensagem_usuario = st.chat_input("Escreva sua mensagem aqui...")

if mensagem_usuario:
    # Mostra mensagem do usuário
    st.chat_message("user").markdown(f"**Você:** {mensagem_usuario}")
    st.session_state["lista_mensagens"].append({"role": "user", "content": mensagem_usuario})

    # Monta prompt
    prompt = "\n".join([f'{m["role"]}: {m["content"]}' for m in st.session_state["lista_mensagens"]])

    # Mostra indicador de “IA digitando...”
    with st.spinner("B.E.T.H está digitando..."):
        time.sleep(1)  # Simula pequeno delay para parecer natural
        try:
            resposta = modelo.generate_content(prompt)
            resposta_ia = resposta.text
        except Exception:
            resposta_ia = "Desculpe, ocorreu um erro. Tente novamente mais tarde."

    # Exibe resposta da IA
    st.chat_message("assistant").markdown(f"**B.E.T.H:** {resposta_ia}")
    st.session_state["lista_mensagens"].append({"role": "assistant", "content": resposta_ia})

    # Atualiza histórico
    st.session_state["historico_chats"][st.session_state.chat_atual] = st.session_state["lista_mensagens"]








