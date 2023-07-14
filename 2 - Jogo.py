import streamlit as st
import mysql.connector
import random
from PIL import Image

primaryColor = "#f73030"
backgroundColor = "#ebf5f3"
secondaryBackgroundColor = "#0fe2cb"
textColor = "#121111"
font = "serif"

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

def display_hangman(chances):
    stages = [
        'Setima.png',
        'Sexta.png',
        'Quinta.png',
        'Quarta.png',
        'Terceira.png',
        'Segunda.png',
        'Primeira.png'
    ]

    if chances < len(stages):
        image_path = stages[chances]
    else:
        image_path = stages[-1]

    image = Image.open(image_path)
    st.image(image)

def obter_usuario(nome, senha):
    conn = mysql.connector.connect(
        host='localhost',
        database='nome',
        user='root',
        password='DAMARIS21$'
    )

    cursor = conn.cursor()
    query = f"SELECT nome, senha FROM cadastro WHERE nome = '{nome}' AND senha = '{senha}'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result



def iniciar_jogo():
    st.subheader('Escolha uma opção de categoria:')
    st.session_state.categoria_escolhida = st.selectbox("", ['fruta', 'animal', 'objeto', 'cor', 'cidades'])
    st.session_state.buttonEscolha = st.button('Gerar')
    if st.session_state.buttonEscolha  == True:
        conn = mysql.connector.connect(
            host='localhost',
            database='nome',
            user='root',
            password='DAMARIS21$'
        )

    # Consulta SQL para obter as palavras da categoria escolhida
        query_palavras = f"SELECT {st.session_state.categoria_escolhida} FROM categoria"
        cursor = conn.cursor()
        cursor.execute(query_palavras)

    # Obter as palavras resultantes
        palavras = [palavra[0] for palavra in cursor.fetchall()]

    # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()
        if 'palavra_selecionada' not in st.session_state:
            st.session_state.palavra_selecionada = random.choice(palavras)
    jogo()


    # Selecionar uma palavra aleatória da lista
def jogo():
    tabuleiro = ['_'] * len(st.session_state.palavra_selecionada)
    letras_tentativas = []
    chances = 6
    i = 0
    erro = 0
    pontuacao = 1000

    while i < 13:
        st.text(display_hangman(chances))
        st.text(tabuleiro)
        st.text(f'Você tem {chances} chances')

        tentativa = st.text_input('Digite uma letra:', key=f'tentativa{i}')
        i += 1
        
        if not tentativa.isalpha():
            st.write('')
            continue

        if tentativa in letras_tentativas:
            st.warning('Você já tentou essa letra. Escolha outra!')
            continue

        letras_tentativas.append(tentativa)

        if tentativa in st.session_state.palavra_selecionada:
            st.success('Você acertou a letra!')
            for j, char in enumerate(st.session_state.palavra_selecionada):
                if char == tentativa:
                    tabuleiro[j] = tentativa

            if "_" not in tabuleiro:
                st.subheader(f'\nVocê venceu! A palavra era: {st.session_state.palavra_selecionada}.')
                pontuacao -= erro
                atualizar_pontuacao(st.session_state.nome, pontuacao)
                break
        else:
            st.error('Ops. Essa letra não está na palavra!')
            erro +=  100
            chances -= 1
        if chances == 0:
            st.text(display_hangman(chances))
            st.subheader(f'\nVocê perdeu! A palavra era: {st.session_state.palavra_selecionada}.')
            pontuacao = 0
            break
            if i < 11:
                st.subheader(f'\nVocê perdeu! A palavra era: {st.session_state.palavra_selecionada}.')
                pontuacao = 0
                break


def main():
    st.subheader('Login')
    nome_login = st.text_input('Nome:')
    senha_login = st.text_input('Senha:', type='password')
    buttonLogin = st.button('Entrar')

    if buttonLogin:
        usuario = obter_usuario(nome_login, senha_login)
        if usuario is not None:
            st.success('Login realizado com sucesso! O jogo vai começar.')
            st.session_state.nome = usuario
            st.session_state.jogo_iniciado = True

def atualizar_pontuacao(nome, pontuacao):
    conn = mysql.connector.connect(
        host='localhost',
        database='nome',
        user='root',
        password='DAMARIS21$'
    )

    cursor = conn.cursor()
    query = "UPDATE cadastro SET pontuacao = %s WHERE nome = %s"
    params = (pontuacao, nome[0])
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

if 'nome' not in st.session_state:
    main()
else:
    iniciar_jogo()
        


