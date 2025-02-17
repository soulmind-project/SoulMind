import streamlit as st
import openai
import docx
import requests

# Configurar a chave da OpenAI/OpenRouter
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

# Função para baixar e ler o arquivo DOCX diretamente do GitHub
def baixar_e_ler_docx(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open("modulo2.docx", "wb") as f:
            f.write(response.content)
        doc = docx.Document("modulo2.docx")
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    else:
        return "⚠️ Não foi possível baixar o conteúdo."

# URL do arquivo no GitHub (ajuste com seu nome de usuário e repositório)
url_arquivo = "https://raw.githubusercontent.com/SEU_USUARIO/soulmind-prototipo/main/modulo2.docx"

# Carregar o conteúdo
conteudo = baixar_e_ler_docx(url_arquivo)

# Interface do Streamlit
st.title("💡 SoulMind - Prototipagem Rápida")

# Exibir o conteúdo carregado
if conteudo:
    st.subheader("📖 Conteúdo Carregado:")
    st.text_area("Texto", conteudo[:2000], height=400)

    # Caixa de perguntas
    pergunta = st.text_input("💬 Digite sua pergunta sobre o conteúdo:")

    # Se houver pergunta
    if st.button("🔍 Perguntar"):
        with st.spinner("⏳ Processando sua pergunta..."):
            try:
                resposta = openai.Completion.create(
                    engine="openai/gpt-3.5-turbo",
                    prompt=f"{conteudo[:3000]}\n\nPergunta: {pergunta}",
                    max_tokens=200
                )
                resposta_texto = resposta['choices'][0]['text'].strip()
                st.success("✅ Resposta da SoulMind:")
                st.markdown(f"**{resposta_texto}**")

            except Exception as e:
                st.error(f"⚠️ Erro: {e}")

    st.info("📢 **Dica:** O conteúdo foi carregado automaticamente do GitHub.")

