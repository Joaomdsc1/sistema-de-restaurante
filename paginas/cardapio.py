import streamlit as st
import pandas as pd
import json
from pathlib import Path
from collections import Counter

# Importa a página de pedidos do outro arquivo
from paginas.pedido import pedido_page

# --- CONSTANTES E CONFIGURAÇÕES ---
PEDIDOS_FILE = Path("pedidos.json")

# --- FUNÇÕES AUXILIARES ---
def carregar_pedidos():
    """Carrega a lista de pedidos do arquivo JSON."""
    if PEDIDOS_FILE.exists():
        with open(PEDIDOS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Retorna lista vazia se o arquivo estiver corrompido ou vazio
    return []

def salvar_pedido(novo_pedido):
    """Adiciona um novo pedido ao arquivo JSON."""
    pedidos = carregar_pedidos()
    pedidos.append(novo_pedido)
    with open(PEDIDOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(pedidos, f, indent=4, ensure_ascii=False)


# --- PÁGINA DO CARDÁPIO ---
def cardapio_page(data):
    """
    Cria a página do cardápio e de realização de pedidos.

    Args:
        data (pd.DataFrame): DataFrame contendo as colunas 'Prato' e 'Preço'.
    """
    st.header("Cardápio Interativo 🍽️")

    if not {'Prato', 'Preço'}.issubset(data.columns):
        st.error("Erro: o DataFrame deve conter as colunas 'Prato' e 'Preço'.")
        return

    left_column, right_column = st.columns(2)

    # Coluna da Esquerda: Cardápio
    with left_column:
        st.subheader("Nosso Cardápio")
        data_formatado = data.copy()
        data_formatado['Preço'] = data_formatado['Preço'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "."))
        st.dataframe(data_formatado, use_container_width=True, hide_index=True)

    # Coluna da Direita: Pedidos
    with right_column:
        st.subheader("Faça seu pedido!")
        st.write("Selecione a quantidade de cada item.")

        # Usar um formulário para agrupar os inputs e o botão
        with st.form(key="pedido_form"):
            selected_items = {}
            for index, row in data.iterrows():
                prato = row['Prato']
                quantity = st.number_input(f"{prato}:", min_value=0, step=1, key=f"quantity_{prato}")
                if quantity > 0:
                    selected_items[prato] = quantity
            
            # Botão de submit dentro do formulário
            submitted = st.form_submit_button("Fazer Pedido", use_container_width=True)

            if submitted and selected_items:
                total_price = 0.0
                # Calcula o preço total baseado nos itens selecionados
                for prato, quantity in selected_items.items():
                    preco_unitario = data.loc[data['Prato'] == prato, 'Preço'].iloc[0]
                    total_price += float(preco_unitario) * quantity

                # Cria o dicionário do novo pedido
                novo_pedido = {
                    "itens": selected_items,
                    "total": total_price,
                    # Adiciona um timestamp para o pedido
                    "data_pedido": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Salva o pedido no arquivo JSON
                salvar_pedido(novo_pedido)
                st.success("Seu pedido foi realizado e salvo com sucesso!")

            elif submitted and not selected_items:
                st.warning("Por favor, selecione pelo menos um item para fazer o pedido.")


# --- APLICAÇÃO PRINCIPAL ---
def main():
    st.title("Sistema de Pedidos do Restaurante")

    # Dados de exemplo para o cardápio
    dados_cardapio = {
        'Prato': ['Pizza Margherita', 'Hambúrguer Clássico', 'Salada Caesar', 'Sushi (8 pçs)', 'Refrigerante'],
        'Preço': [45.50, 28.00, 22.00, 35.00, 6.50]
    }
    df_cardapio = pd.DataFrame(dados_cardapio)

    # Menu de navegação na barra lateral
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Escolha uma página", ["Cardápio e Pedir", "Ver Pedidos Salvos"])

    if page == "Cardápio e Pedir":
        cardapio_page(df_cardapio)
    elif page == "Ver Pedidos Salvos":
        pedido_page() # Esta função vem do arquivo pedidos_page.py

if __name__ == "__main__":
    main()
