import csv
import os

# Dados para o arquivo CSV
data = [
    {"Número": 1, "Prato": "Creme de Açaí Pequeno", "Preço": 10.00, "Tamanho": "300ml"},
    {"Número": 2, "Prato": "Creme de Açaí Médio", "Preço": 15.00, "Tamanho": "500ml"},
    {"Número": 3, "Prato": "Creme de Açaí Grande", "Preço": 20.00, "Tamanho": "700ml"},
    {"Número": 4, "Prato": "Milk Shake Pequeno", "Preço": 18.00, "Tamanho": "300ml"},
    {"Número": 5, "Prato": "Milk Shake Grande", "Preço": 12.00, "Tamanho": "500ml"},
]

# Nome do arquivo CSV
# Criar o diretório 'csv' se não existir
os.makedirs("csv", exist_ok=True)
file_name = "csv/cardapio.csv"

# Gerar o arquivo CSV
with open(file_name, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Número", "Prato", "Preço", "Tamanho"])
    writer.writeheader()
    writer.writerows(data)

print(f"Arquivo '{file_name}' gerado com sucesso!")