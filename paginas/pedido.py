import streamlit as st
import json
from pathlib import Path

# O nome do arquivo deve ser o mesmo usado no app.py
PEDIDOS_FILE = Path("pedidos.json")

def carregar_pedidos():
    """Carrega a lista de pedidos do arquivo JSON."""
    if PEDIDOS_FILE.exists():
        with open(PEDIDOS_FILE, 'r', encoding='utf-8') as f:
            try:
                # Carrega os dados do arquivo
                return json.load(f)
            except json.JSONDecodeError:
                # Retorna uma lista vazia se o arquivo estiver vazio ou for inválido
                return []
    return []

def pedido_page():
    """
    Cria a página que exibe todos os pedidos salvos do arquivo JSON.
    """
    st.header("Controle de Pedidos Salvos 📋")
    st.write("Aqui estão todos os pedidos que foram realizados e salvos no sistema.")

    # Botão para recarregar os pedidos do arquivo
    if st.button("Atualizar Lista de Pedidos"):
        st.rerun()

    pedidos_salvos = carregar_pedidos()

    if not pedidos_salvos:
        st.info("Ainda não há pedidos salvos. Vá para a página de cardápio para fazer um novo pedido.")
    else:
        # Exibe os pedidos em ordem inversa (o mais novo primeiro)
        for i, pedido in enumerate(reversed(pedidos_salvos)):
            # Formata o total para exibição
            total_formatado = f"R$ {pedido['total']:,.2f}".replace(",", ".")
            
            # Usa um expander para cada pedido
            with st.expander(f"**Pedido #{len(pedidos_salvos) - i}** | Data: {pedido.get('data_pedido', 'N/A')} | Total: {total_formatado}"):
                st.write("**Itens do Pedido:**")
                for prato, quantity in pedido['itens'].items():
                    st.write(f"- {quantity}x **{prato}**")
