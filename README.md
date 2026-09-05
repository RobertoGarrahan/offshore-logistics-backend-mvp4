# Offshore Logistics API (Back-End) - MVP4

API RESTful conteinerizada desenvolvida para o MVP de Arquitetura de Software (Cenário 1.1). O sistema gerencia o cadastro de fornecedores logísticos do setor naval e fornece dados climáticos de portos estratégicos.

## Tecnologias Utilizadas
* **Linguagem:** Python 3.10
* **Framework:** Flask
* **Banco de Dados:** SQLite (Embutido)
* **Integração Externa:** Open-Meteo API (Previsão do tempo)
* **Deploy:** Docker

## Como Executar (Docker)
1. Construa a imagem da API:
   `docker build -t offshore-api .`
2. Execute o container na porta 5000:
   `docker run -p 5000:5000 offshore-api`

## Rotas Disponíveis
* `GET /fornecedores` - Lista todos os fornecedores homologados.
* `POST /fornecedores` - Cadastra um novo fornecedor.
* `PUT /fornecedores/<id>` - Atualiza os dados de um fornecedor.
* `DELETE /fornecedores/<id>` - Remove um fornecedor do sistema.
* `GET /porto/clima?lat={lat}&lon={lon}` - Retorna as condições climáticas atuais das coordenadas informadas.

![Fluxograma de Arquitetura do Sistema](./arquitetura.png)