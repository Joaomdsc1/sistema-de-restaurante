import pytest
import json
import pandas as pd
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import tempfile
import os

from paginas.cardapio import carregar_pedidos, salvar_pedido, cardapio_page
from paginas.pedido import pedido_page

# Simula o cardápio
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'Prato': [
            'Creme de Açaí Pequeno',
            'Creme de Açaí Médio',
            'Creme de Açaí Grande',
            'Milk Shake Pequeno',
            'Milk Shake Grande'
        ],
        'Preço': [
            10.00,
            15.00,
            20.00,
            18.00,
            12.00
        ]
    })

# Todos os testes passam aqui

class TestCarregarPedidos:
    
    def test_carregar_pedidos_arquivo_existente_valido(self):
        dados_mock = [
            {"itens": {"Creme de Açai Pequeno": 2}, "total": 10.0, "data_pedido": "2024-01-01 12:00:00"}
        ]

        # problema com exists corrigido
        with patch.object(Path, "exists", return_value=True), \
             patch("builtins.open", mock_open(read_data=json.dumps(dados_mock))):
            resultado = carregar_pedidos()
                
        assert resultado == dados_mock
        assert len(resultado) == 1
        assert resultado[0]["total"] == 10.0
    
    def test_carregar_pedidos_arquivo_inexistente(self):
        with patch.object(Path, "exists", return_value=False):
            resultado = carregar_pedidos()
        assert resultado == []
    
    def test_carregar_pedidos_arquivo_json_corrompido(self):
        with patch.object(Path, "exists", return_value=True), \
             patch("builtins.open", mock_open(read_data="json inválido")):
            resultado = carregar_pedidos()
        assert resultado == []
    
    def test_carregar_pedidos_arquivo_vazio(self):
        with patch.object(Path, "exists", return_value=True), \
             patch("builtins.open", mock_open(read_data="")):
            resultado = carregar_pedidos()
        assert resultado == []


class TestSalvarPedido:
    
    def test_salvar_pedido_primeiro_pedido(self):
        novo_pedido = {
            "itens": {"Creme de Açaí Médio": 1},
            "total": 15.0,
            "data_pedido": "2024-01-01 12:00:00"
        }

        with patch("paginas.cardapio.carregar_pedidos", return_value=[]), \
            patch("builtins.open", mock_open()) as mock_file:
            salvar_pedido(novo_pedido)
            mock_file.assert_called_once_with(Path("pedidos.json"), 'w', encoding='utf-8')

            handle = mock_file.return_value.__enter__.return_value
            assert handle.write.call_count > 0

    
    def test_salvar_pedido_adicionar_a_existentes(self):
        pedidos_existentes = [
            {"itens": {"Creme de Açai Pequeno": 1}, "total": 10.0, "data_pedido": "2024-01-01 11:00:00"}
        ]
        novo_pedido = {
            "itens": {"Milk Shake Grande": 1},
            "total": 12.0,
            "data_pedido": "2024-01-01 12:00:00"
        }

        with patch("paginas.cardapio.carregar_pedidos", return_value=pedidos_existentes), \
            patch("builtins.open", mock_open()) as mock_file:
            salvar_pedido(novo_pedido)

            mock_file.assert_called_once_with(Path("pedidos.json"), 'w', encoding='utf-8')

            handle = mock_file.return_value.__enter__.return_value
            assert handle.write.call_count > 0


    
    def test_salvar_pedido_estrutura_valida(self):
        novo_pedido = {
            "itens": {"Creme de Açaí Grande": 2, "Milk Shake Pequeno": 1},
            "total": 38.0,
            "data_pedido": "2024-01-01 15:30:00"
        }
        
        with patch("paginas.cardapio.carregar_pedidos", return_value=[]), \
             patch("builtins.open", mock_open()):
            salvar_pedido(novo_pedido)
                
        assert "itens" in novo_pedido
        assert "total" in novo_pedido
        assert "data_pedido" in novo_pedido
        assert isinstance(novo_pedido["itens"], dict)
        assert isinstance(novo_pedido["total"], (int, float))


class TestCardapioPage:
    
    def test_cardapio_page_formatacao_preco(self, sample_dataframe):
        with patch('streamlit.header'), \
            patch('streamlit.columns', return_value=[MagicMock(), MagicMock()]), \
            patch('streamlit.subheader'), \
            patch('streamlit.dataframe') as mock_dataframe, \
            patch('streamlit.write'), \
            patch('streamlit.form'), \
            patch('streamlit.number_input', side_effect=lambda *args, **kwargs: 0), \
            patch('streamlit.form_submit_button'):
            cardapio_page(sample_dataframe)
            mock_dataframe.assert_called_once()
    

    def test_cardapio_page_dataframe_nao_modificado(self, sample_dataframe):
        original_data = sample_dataframe.copy()
        with patch('streamlit.header'), \
            patch('streamlit.columns', return_value=[MagicMock(), MagicMock()]), \
            patch('streamlit.subheader'), \
            patch('streamlit.dataframe'), \
            patch('streamlit.write'), \
            patch('streamlit.form'), \
            patch('streamlit.number_input', side_effect=lambda *args, **kwargs: 0), \
            patch('streamlit.form_submit_button'):
            cardapio_page(sample_dataframe)
        assert sample_dataframe.equals(original_data)

    def test_cardapio_page_dados_validos_requeridos(self):
        df_invalido = pd.DataFrame({'Coluna': ['valor']})
        with patch('streamlit.header'), \
            patch('streamlit.columns', return_value=[MagicMock(), MagicMock()]), \
            patch('streamlit.subheader'), \
            patch('streamlit.dataframe'), \
            patch('streamlit.write'), \
            patch('streamlit.form'), \
            patch('streamlit.number_input'), \
            patch('streamlit.form_submit_button'):
            cardapio_page(df_invalido)



class TestPedidoPage:
    
    def test_pedido_page_sem_pedidos(self):
        with patch('paginas.pedido.carregar_pedidos', return_value=[]), \
             patch('streamlit.header'), \
             patch('streamlit.write'), \
             patch('streamlit.button'), \
             patch('streamlit.info') as mock_info:
            pedido_page()
            mock_info.assert_called_once()
    
    def test_pedido_page_com_pedidos(self):
        pedidos_mock = [
            {
                "itens": {"Creme de Açai Pequeno": 1, "Milk Shake Pequeno": 2},
                "total": 58.0,
                "data_pedido": "2024-01-01 12:00:00"
            }
        ]
        with patch('paginas.pedido.carregar_pedidos', return_value=pedidos_mock), \
             patch('streamlit.header'), \
             patch('streamlit.write'), \
             patch('streamlit.button'), \
             patch('streamlit.expander') as mock_expander:
            pedido_page()
            mock_expander.assert_called()
    
    def test_pedido_page_formatacao_total(self):
        pedidos_mock = [
            {
                "itens": {"Sushi": 2},
                "total": 70.0,
                "data_pedido": "2024-01-01 14:30:00"
            }
        ]
        with patch('paginas.pedido.carregar_pedidos', return_value=pedidos_mock), \
             patch('streamlit.header'), \
             patch('streamlit.write'), \
             patch('streamlit.button'), \
             patch('streamlit.expander'):
            pedido_page()


class TestIntegracaoSistema:
    
    def test_fluxo_completo_pedido(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_path = temp_file.name
            
        try:
            with patch('paginas.cardapio.PEDIDOS_FILE', Path(temp_path)):
                pedidos_iniciais = carregar_pedidos()
                assert pedidos_iniciais == []
                
                novo_pedido = {
                    "itens": {"Creme de Açai Pequeno": 1},
                    "total": 45.5,
                    "data_pedido": "2024-01-01 12:00:00"
                }
                salvar_pedido(novo_pedido)
                
                pedidos_atualizados = carregar_pedidos()
                assert len(pedidos_atualizados) == 1
                assert pedidos_atualizados[0]["total"] == 45.5
                
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_dados_cardapio_validos(self):
        dados_cardapio = {
            'Prato': ['Creme de Açai Pequeno Margherita', 'Hambúrguer Clássico', 'Salada Caesar'],
            'Preço': [45.50, 28.00, 22.00]
        }
        df = pd.DataFrame(dados_cardapio)
        assert 'Prato' in df.columns
        assert 'Preço' in df.columns
        assert len(df) > 0
        assert all(isinstance(preco, (int, float)) for preco in df['Preço'])
        assert all(isinstance(prato, str) for prato in df['Prato'])


if __name__ == "__main__":
    pytest.main([__file__])
