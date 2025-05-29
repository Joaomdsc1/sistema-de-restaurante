import streamlit as st



def cardapio_page(data):
    st.title("Bem-vindo ao Cardápio!")
    left_column, right_column = st.columns(2)
    left_column.title("Cardápio")
    
    data_formatado = data.copy()

    # Formatando a coluna preço para incluir "R$" e duas casas decimais
    data_formatado['Preço'] = data_formatado['Preço'].apply(lambda x: f"R$ {x:.2f}")
    
    left_column.dataframe(data_formatado)
    right_column.title("Faça seu pedido!")
    right_column.write("Selecione os produtos do seu pedido.")
    
    # Adicionando um campo para selecionar múltiplos itens do mesmo prato
    selected_items = []
    for prato in data['Prato'].tolist():
        quantity = right_column.number_input(f"{prato}:", min_value=0, step=1, key=f"quantity_{prato}")
        if quantity > 0:
            selected_items.extend([prato] * quantity)
    
    if selected_items:
        right_column.write("Você selecionou:")
        for item in selected_items:
            right_column.write(item)

        total_price = sum(float(data[data['Prato'] == prato]['Preço']) for prato in selected_items)
        right_column.write(f"Preço total: R$ {total_price:.2f}")