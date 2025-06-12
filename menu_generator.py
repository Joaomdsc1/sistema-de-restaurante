import csv
import os

def generate_csv():
    # Dados para o arquivo CSV
    data = [
        {"Número": 1, "Nome": "Creme de Açaí Pequeno", "Preço": 10.00, "Tamanho": "300ml"},
        {"Número": 2, "Nome": "Creme de Açaí Médio", "Preço": 15.00, "Tamanho": "500ml"},
        {"Número": 3, "Nome": "Creme de Açaí Grande", "Preço": 20.00, "Tamanho": "700ml"},
        {"Número": 4, "Nome": "Milk Shake Pequeno", "Preço": 18.00, "Tamanho": "300ml"},
        {"Número": 5, "Nome": "Milk Shake Grande", "Preço": 12.00, "Tamanho": "500ml"},
    ]

    # Nome do arquivo CSV
    # Criar o diretório 'csv' se não existir
    os.makedirs("csv", exist_ok=True)
    file_name = "csv/cardapio.csv"

    # Gerar o arquivo CSV
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Número", "Nome", "Preço", "Tamanho"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Arquivo '{file_name}' gerado com sucesso!")

def add_item_to_csv():
    item = get_info_to_item()
    # Nome do arquivo CSV
    file_name = "csv/cardapio.csv"
    # Verificar se o arquivo já existe
    if not os.path.exists(file_name):
        print(f"Arquivo '{file_name}' não encontrado. Gerando novo arquivo...")
        generate_csv()
    # Adicionar o item ao arquivo CSV
    with open(file_name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Número", "Nome", "Preço", "Tamanho"])
        # Obter o número do próximo item
        next_number = sum(1 for row in csv.DictReader(open(file_name, encoding="utf-8"))) + 1
        item["Número"] = next_number
        writer.writerow(item)
    print(f"Item '{item['Nome']}' adicionado com sucesso ao arquivo '{file_name}'!")
    
    
def get_info_to_item():
    # Solicitar informações do usuário
    name = str(input("Nome do item: "))
    price = float(input("Preço do item: "))
    size = str(input("Tamanho do item: "))

    return {
        "Nome": name,
        "Preço": price,
        "Tamanho": size
    }

def add_items_to_csv():
    while True:
        add_item_to_csv()
        another = input("Deseja adicionar outro item? (s/n): ").strip().lower()
        if another != 's':
            break
    print("Todos os itens foram adicionados com sucesso!")

if __name__ == "__main__":
    print("Qual ação você deseja realizar?")
    action = input("1. Gerar CSV\n2. Adicionar itens ao CSV\nEscolha uma opção (1 ou 2): ")
    if action == "1":
        generate_csv()
    elif action == "2":
        add_items_to_csv()
    else:
        print("Opção inválida. Por favor, escolha 1 ou 2.")