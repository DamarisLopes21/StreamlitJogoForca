from PIL import Image
import streamlit as st
import pandas as pd
import mysql.connector


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


# Conectar-se ao banco de dados MySQL
conn = mysql.connector.connect(
    host='localhost',
    database='nome',
    user='root',
    password='DAMARIS21$'
)

# Consulta SQL para obter os dados dos jogadores
query = "SELECT nome, pontuacao FROM cadastro ORDER BY pontuacao DESC"
cursor = conn.cursor()
cursor.execute(query)
result = cursor.fetchall()

# Criar uma lista de dicionários com os dados dos jogadores
jogadores = [{'Nome': row[0], 'Pontuação': row[1]} for row in result]

# Criar DataFrame a partir dos dados
df = pd.DataFrame(jogadores)

i = 0
# Ordenar os jogadores por pontuação (do maior para o menor)
df = df.sort_values('Pontuação', ascending=False)

# Adicionar uma coluna para destacar os três primeiros colocados
df['Colocação'] = range(1, len(df) + 1)
df['Colocação'] = df['Colocação'].apply(lambda x: f'{x}°' )

# Exibir o ranking de jogadores
st.title('Ranking de Jogadores')
st.table(df)
