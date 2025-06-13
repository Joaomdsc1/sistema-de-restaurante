# SITE DE VENDAS DE AÇAÍ

## 1. Nome dos Membros do Grupo
- Alícia Marzola Chaves
- José Gabriel Vieira de Souza
- João Guilherme Marcondes de Souza Costa

## 2. Explicação do Sistema

Esse repositório armazena a implementação do trabalho prático da disciplina de Engenharia de Software II - DCC072 da Universidade Federal de Minas Gerais (UFMG).

O projeto tem como objetivo aplicar os conceitos abordados ao longo da disciplina por meio do desenvolvimento de um website escolhido pelo grupo, que simula uma loja virtual de açaí.

A aplicação permite aos usuários:
* Consultar o cardápio disponível;
* Realizar pedidos de forma prática;
* Visualizar pedidos anteriores;
* Acessar informações sobre a loja, incluindo formas de contato.

### Como Iniciar o Site

Para colocar o projeto em execução em sua máquina local, siga os passos abaixo.

#### Pré-requisitos

Certifique-se de ter os seguintes softwares instalados:

* **Python 3.12.3** (versões anteriores podem funcionar, mas não é garantido funcionamento com as dependências).
* **pip** (geralmente vem com o Python).

#### Configuração do Backend

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Joaomdsc1/sistema-de-restaurante](https://github.com/Joaomdsc1/sistema-de-restaurante)
    cd sistema-de-restaurante # Navegue para a pasta raiz do projeto clonado
    ```

2.  **Crie e Ative o Ambiente Virtual:**
    É altamente recomendado criar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    python3 -m venv venv
    ```
    * **No Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **No macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Instale as Dependências:**
    Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4. **Inicie o Site:**
    ```bash
    streamlit run app.py # Ou o comando para iniciar seu arquivo principal do backend
    ```

## 3. Explicação das tecnologias utilizadas

**Streamlit**

Streamlit foi usado para criar a interface gráfica do sistema, permitindo a navegação entre páginas e a realização de pedidos.

* Utilizado para montar páginas como cardápio, pedido, sobre e contato com componentes interativos.
* Permite exibir tabelas, formulários e mensagens dinâmicas conforme as ações do usuário.

**Pandas**


Pandas foi usado para manipular o cardápio e calcular os totais dos pedidos.

* Leu os dados do cardápio a partir de um arquivo CSV para exibição e uso nos pedidos.
* Realizou o cálculo do valor total de cada pedido com base na quantidade e preço de cada item.

**JSON**

O formato JSON foi usado para armazenar os pedidos realizados pelos usuários.

* Guardou cada pedido como um dicionário dentro de uma lista salva no arquivo pedidos.json.
* Permitiu persistir as informações dos pedidos mesmo após o sistema ser fechado.

**Pytest**

Pytest foi utilizado para testar automaticamente as funcionalidades do sistema.

* Verificou se os pedidos estão sendo carregados e salvos corretamente.
* Testou o comportamento da interface simulando ações do usuário com mocks.

**Unittest.mock**

Unittest.mock foi usado nos testes para simular leitura e escrita de arquivos e ações do Streamlit.

* Evitou acessar arquivos reais, simulando a função open e a presença do arquivo pedidos.json.
* Simulou os componentes da interface (como botão e formulário) para testar o código da página.

