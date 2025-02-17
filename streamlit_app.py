import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import docx
import torch

# Carregar o modelo da Hugging Face (Open Source)
@st.cache_resource
def carregar_modelo():
    model_name = "mistralai/Mistral-7B-Instruct-v0.1"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

# Função para ler o arquivo DOCX
def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

# Interface no Streamlit
st.title("💡 SoulMind - Modo Open Source 🛠️")

# Upload do arquivo
uploaded_file = st.file_uploader("📂 Envie o arquivo DOCX", type="docx")

if uploaded_file is not None:
    # Ler e exibir o conteúdo
    conteudo = read_docx(uploaded_file)
    st.subheader("📖 Conteúdo Carregado:")
    st.text_area("Texto", conteudo[:2000], height=400)

    # Campo para perguntas
    pergunta = st.text_input("💬 Digite sua pergunta sobre o conteúdo:")

    if st.button("🔍 Perguntar"):
        st.warning("⏳ Processando... Aguarde, pode levar alguns segundos.")
        try:
            # Carregar o modelo e gerar a resposta
            model, tokenizer = carregar_modelo()
            input_text = f"{conteudo[:1500]}\n\nPergunta: {pergunta}"
            inputs = tokenizer(input_text, return_tensors="pt")
            with torch.no_grad():
                output = model.generate(**inputs, max_length=300)
            resposta = tokenizer.decode(output[0], skip_special_tokens=True)

            # Exibir a resposta
            st.success("✅ Resposta da SoulMind:")
            st.write(resposta)

        except Exception as e:
            st.error(f"⚠️ Erro durante o processamento: {e}")

st.info("📢 Modo gratuito e 100% open source ativado! 🚀")


