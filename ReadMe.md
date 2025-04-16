# Exercício 1 - BD2

## Descrição:
O projeto tem como objetivo consolidar os conhecimentos quanto a SQL injection, DAO (Data 
Access Object) e a conexão entre a aplicação e o banco de dados, no caso desse sistema foi utilizado o PgMyAdmin.

## Tecnologias Utilizadas
- Html e css
- Python
- Postgres

## Como Executar
1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   ```
2. Navegue até a pasta `./ORM` ou `./Driver`:
   ```bash
   cd ./ORM
   # ou
   cd ./Driver
   ```
3. Execute o arquivo `app.py` presente na pasta escolhida:
   ```bash
   python app.py
   ```
   **Nota:** Execute apenas um dos métodos por vez (`ORM` ou `Driver`), pois ambos utilizam o mesmo front-end, mas implementam diferentes formas de conexão com o banco de dados.

## Descrição da aplicação
No arquivo `app.py` presente na pasta `Driver`, existe a possibilidade de ativar o modo vulnerável ao SQL Injection. Essa funcionalidade foi implementada para fins educacionais, permitindo que o usuário entenda como ataques de SQL Injection podem ocorrer e como evitá-los. Por outro lado, o modelo `ORM` (Object-Relational Mapping) não possui essa opção de vulnerabilidade, pois utiliza abstrações que geram as consultas SQL de forma segura, evitando a manipulação direta de strings SQL. Dessa forma, o uso de ORMs reduz significativamente o risco de ataques de SQL Injection, já que os parâmetros das consultas são tratados de maneira segura e automatizada.

A aplicação permite a inserção de um novo pedido no banco de dados **Northwind**. Além disso, ela implementa dois relatórios principais. O primeiro relatório exibe informações completas sobre um pedido, como número do pedido, data, cliente, vendedor e itens relacionados. O segundo relatório apresenta um ranking dos funcionários em um intervalo de tempo específico, considerando o total de pedidos realizados e a soma dos valores vendidos.

## Créditos
Este projeto foi desenvolvido por **Pedro Reimberg - 2023006537** e **Paulo Vitor - 2023006359**.