import streamlit as st
from PIL import Image

primaryColor="#f73030"
backgroundColor="#ebf5f3"
secondaryBackgroundColor="#0fe2cb"
textColor="#121111"
font="serif"


st.set_page_config(
    page_title='Enigma Lexical',
    page_icon='Tela.png',
    layout='wide'
)


image = Image.open("Logo1.png")

# Redimensiona a imagem para um tamanho menor
width, height = image.size
max_width = 180  # Define a largura máxima desejada
if width > max_width:
    ratio = max_width / width
    new_size = (int(width * ratio), int(height * ratio))
    image.thumbnail(new_size)

# Exibe a imagem redimensionada
st.image(image)

st.title("Enigma lexical")

st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<h1 class="title">Bem-vindo ao Jogo da Forca!</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Cadastre-se para começar a jogar:</div>', unsafe_allow_html=True)

