# SITE DE VENDAS DE AÇAÍ

Esse repositório armazena a implementação do trabalho prático da disciplina de Engenharia de Software II - DCC072 da Universidade Federal de Minas Gerais (UFMG).

O objetivo desse projeto é trabalhar os conceitos vistos na disciplina através da criação de um website, escolhido pelo grupo, que representa uma loja de açaí virtual.

## Sumário

* [Iniciando o Site](#iniciando-o-site)

## Iniciando o Site

Para colocar o projeto em execução em sua máquina local, siga os passos abaixo.

### Pré-requisitos

Certifique-se de ter os seguintes softwares instalados:

* **Python 3.12.3** (versões anteriores podem funcionar, mas não é garantido funcionamento com as dependências).
* **pip** (geralmente vem com o Python).

### Configuração do Backend

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
