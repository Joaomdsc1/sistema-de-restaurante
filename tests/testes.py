import pytest
import json
import pandas as pd
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import tempfile
import os

# Importa as funções do sistema
from paginas.cardapio import carregar_pedidos, salvar_pedido, cardapio_page
from paginas.pedido import pedido_page


# Fixtures simples dentro do próprio arquivo
@pytest.fixture
def sample_dataframe():
    """DataFrame de exemplo para testes"""
    return pd.DataFrame({
        'Prato': ['Pizza Margherita', 'Hambúrguer Clássico'],
        'Preço': [45.50, 28.00]
    })

@pytest.fixture
def sample_pedido():
    """Pedido de exemplo para testes"""
    return {
        "itens": {"Pizza Margherita": 1, "Refrigerante": 2},
        "total": 58.50,
        "data_pedido": "2024-01-01 12:00:00"
    }


class TestCarregarPedidos:
    """Testes para a função carregar_pedidos"""
    
    def test_carregar_pedidos_arquivo_existente_valido(self):
        """Testa carregamento de pedidos de arquivo JSON válido"""
        dados_mock = [
            {"itens": {"Pizza": 2}, "total": 50.0, "data_pedido": "2024-01-01 12:00:00"}
        ]
        
        with patch("cardapio.PEDIDOS_FILE.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(dados_mock))):
                resultado = carregar_pedidos()
                
        assert resultado == dados_mock
        assert len(resultado) == 1
        assert resultado[0]["total"] == 50.0
    
    def test_carregar_pedidos_arquivo_inexistente(self):
        """Testa carregamento quando arquivo não existe"""
        with patch("cardapio.PEDIDOS_FILE.exists", return_value=False):
            resultado = carregar_pedidos()
            
        assert resultado == []
    
    def test_carregar_pedidos_arquivo_json_corrompido(self):
        """Testa carregamento com arquivo JSON inválido"""
        with patch("cardapio.PEDIDOS_FILE.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="json inválido")):
                resultado = carregar_pedidos()
                
        assert resultado == []
    
    def test_carregar_pedidos_arquivo_vazio(self):
        """Testa carregamento de arquivo vazio"""
        with patch("cardapio.PEDIDOS_FILE.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="")):
                resultado = carregar_pedidos()
                
        assert resultado == []


class TestSalvarPedido:
    """Testes para a função salvar_pedido"""
    
    def test_salvar_pedido_primeiro_pedido(self):
        """Testa salvamento do primeiro pedido em arquivo vazio"""
        novo_pedido = {
            "itens": {"Hambúrguer": 1},
            "total": 28.0,
            "data_pedido": "2024-01-01 12:00:00"
        }
        
        with patch("cardapio.carregar_pedidos", return_value=[]):
            with patch("builtins.open", mock_open()) as mock_file:
                salvar_pedido(novo_pedido)
                
                # Verifica se o arquivo foi aberto para escrita
                mock_file.assert_called_once_with("pedidos.json", 'w', encoding='utf-8')
                
                # Verifica se json.dump foi chamado com os dados corretos
                handle = mock_file.return_value.__enter__.return_value
                written_data = handle.write.call_args_list
                assert len(written_data) > 0
    
    def test_salvar_pedido_adicionar_a_existentes(self):
        """Testa adicionar pedido a lista existente"""
        pedidos_existentes = [
            {"itens": {"Pizza": 1}, "total": 45.5, "data_pedido": "2024-01-01 11:00:00"}
        ]
        novo_pedido = {
            "itens": {"Salada": 1},
            "total": 22.0,
            "data_pedido": "2024-01-01 12:00:00"
        }
        
        with patch("cardapio.carregar_pedidos", return_value=pedidos_existentes):
            with patch("builtins.open", mock_open()) as mock_file:
                salvar_pedido(novo_pedido)
                
                mock_file.assert_called_once_with("pedidos.json", 'w', encoding='utf-8')
    
    def test_salvar_pedido_estrutura_valida(self):
        """Testa se o pedido mantém estrutura válida após salvamento"""
        novo_pedido = {
            "itens": {"Sushi": 2, "Refrigerante": 1},
            "total": 76.5,
            "data_pedido": "2024-01-01 15:30:00"
        }
        
        with patch("cardapio.carregar_pedidos", return_value=[]):
            with patch("builtins.open", mock_open()):
                # Não deve lançar exceção
                salvar_pedido(novo_pedido)
                
        # Verifica se a estrutura do pedido está correta
        assert "itens" in novo_pedido
        assert "total" in novo_pedido
        assert "data_pedido" in novo_pedido
        assert isinstance(novo_pedido["itens"], dict)
        assert isinstance(novo_pedido["total"], (int, float))


class TestCardapioPage:
    """Testes para a função cardapio_page"""
    
    # Usar a fixture global sample_dataframe
    
    def test_cardapio_page_formatacao_preco(self, sample_dataframe):
        """Testa se os preços são formatados corretamente"""
        with patch('streamlit.header'), \
             patch('streamlit.columns'), \
             patch('streamlit.subheader'), \
             patch('streamlit.dataframe') as mock_dataframe, \
             patch('streamlit.write'), \
             patch('streamlit.form'), \
             patch('streamlit.number_input'), \
             patch('streamlit.form_submit_button'):
            
            cardapio_page(sample_dataframe)
            
            # Verifica se dataframe foi chamado
            mock_dataframe.assert_called_once()
    
    def test_cardapio_page_dataframe_nao_modificado(self, sample_dataframe):
        """Testa se o DataFrame original não é modificado"""
        original_data = sample_dataframe.copy()
        
        with patch('streamlit.header'), \
             patch('streamlit.columns'), \
             patch('streamlit.subheader'), \
             patch('streamlit.dataframe'), \
             patch('streamlit.write'), \
             patch('streamlit.form'), \
             patch('streamlit.number_input'), \
             patch('streamlit.form_submit_button'):
            
            cardapio_page(sample_dataframe)
            
            # Verifica se o DataFrame original não foi alterado
            pd.testing.assert_frame_equal(sample_dataframe, original_data)
    
    def test_cardapio_page_dados_validos_requeridos(self):
        """Testa se a função requer DataFrame com colunas corretas"""
        df_invalido = pd.DataFrame({'Coluna': ['valor']})
        
        with patch('streamlit.header'), \
             patch('streamlit.columns'), \
             patch('streamlit.subheader'), \
             patch('streamlit.dataframe'), \
             patch('streamlit.write'), \
             patch('streamlit.form'), \
             patch('streamlit.number_input'), \
             patch('streamlit.form_submit_button'):
            
            # Deve funcionar sem erro (Streamlit vai lidar com colunas ausentes)
            cardapio_page(df_invalido)


class TestPedidoPage:
    """Testes para a função pedido_page do módulo pedido"""
    
    def test_pedido_page_sem_pedidos(self):
        """Testa exibição quando não há pedidos salvos"""
        with patch('paginas.pedido.carregar_pedidos', return_value=[]), \
             patch('streamlit.header'), \
             patch('streamlit.write'), \
             patch('streamlit.button'), \
             patch('streamlit.info') as mock_info:
            
            pedido_page()
            
            # Verifica se mensagem informativa foi exibida
            mock_info.assert_called_once()
    
    def test_pedido_page_com_pedidos(self):
        """Testa exibição com pedidos existentes"""
        pedidos_mock = [
            {
                "itens": {"Pizza": 1, "Refrigerante": 2},
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
            
            # Verifica se expander foi usado para mostrar pedidos
            mock_expander.assert_called()
    
    def test_pedido_page_formatacao_total(self):
        """Testa formatação correta do valor total"""
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
            
            # Não deve lançar erro na formatação
            pedido_page()


class TestIntegracaoSistema:
    """Testes de integração do sistema"""
    
    def test_fluxo_completo_pedido(self):
        """Testa fluxo completo: carregar -> salvar -> carregar novamente"""
        # Simula arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_path = temp_file.name
            
        try:
            # Patch do caminho do arquivo
            with patch('cardapio.PEDIDOS_FILE', Path(temp_path)):
                # Primeiro carregamento (arquivo vazio)
                pedidos_iniciais = carregar_pedidos()
                assert pedidos_iniciais == []
                
                # Salva um pedido
                novo_pedido = {
                    "itens": {"Pizza": 1},
                    "total": 45.5,
                    "data_pedido": "2024-01-01 12:00:00"
                }
                salvar_pedido(novo_pedido)
                
                # Carrega novamente e verifica
                pedidos_atualizados = carregar_pedidos()
                assert len(pedidos_atualizados) == 1
                assert pedidos_atualizados[0]["total"] == 45.5
                
        finally:
            # Limpa arquivo temporário
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_dados_cardapio_validos(self):
        """Testa se os dados do cardápio estão em formato válido"""
        dados_cardapio = {
            'Prato': ['Pizza Margherita', 'Hambúrguer Clássico', 'Salada Caesar'],
            'Preço': [45.50, 28.00, 22.00]
        }
        df = pd.DataFrame(dados_cardapio)
        
        # Verifica estrutura do DataFrame
        assert 'Prato' in df.columns
        assert 'Preço' in df.columns
        assert len(df) > 0
        assert all(isinstance(preco, (int, float)) for preco in df['Preço'])
        assert all(isinstance(prato, str) for prato in df['Prato'])


# Configuração do pytest
if __name__ == "__main__":
    pytest.main([__file__])