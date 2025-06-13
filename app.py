import streamlit as st
import pandas as pd
import numpy as np
from paginas.cardapio import cardapio_page
from paginas.pedido import pedido_page
from paginas.sobre import sobre_page
from paginas.contato import contato_page

st.set_page_config(layout="wide")

# Itens na barra lateral
st.sidebar.image("images/logo.png", use_container_width=True)
st.sidebar.header("Bem-vindo ao Nosso Açaí!")

# Importando os dados do arquivo pratos.csv
data = pd.read_csv('csv/cardapio.csv') 

pages = {
    "Cardápio": lambda: cardapio_page(data),
    "Pedido": lambda: pedido_page(),
    "Sobre": lambda: sobre_page(),
    "Contato": lambda: contato_page()
}

# Exibindo o conteúdo da página selecionada
selected_page = st.sidebar.selectbox("Escolha uma página:", list(pages.keys()))
pages[selected_page]()