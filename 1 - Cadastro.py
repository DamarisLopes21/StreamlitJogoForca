import streamlit as st
import mysql.connector
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

def insert_user(nome, senha):
    conn = mysql.connector.connect(
        host='localhost',
        database='nome',
        user='root',
        password='DAMARIS21$'
    )

    cursor = conn.cursor()
    query = "INSERT INTO cadastro (nome, senha) VALUES (%s, %s)"
    cursor.execute(query, (nome, senha))
    conn.commit()

    cursor.close()
    conn.close()

# Configuração da página de cadastro

st.title("Página de Cadastro")

nome = st.text_input("Nome")
senha = st.text_input("Senha", type="password")

if st.button("Cadastrar"):
    insert_user(nome, senha)
    st.success("Cadastro realizado com sucesso!")
