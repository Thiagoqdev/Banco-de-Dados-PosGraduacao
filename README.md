# Sistema de Gestão de Vendas - Dashboard Integrado

**Desenvolvido por:**  
Thiago Vinicius dos Santos Queiroz — RGM: 36995142  
Lucas Vynicius Gonçalves Albuquerque — RGM: 39905535

---

## 📋 Descrição

Sistema completo para **gestão de vendas, clientes e produtos**, com dashboard integrado.  
Desenvolvido em **Python (Flask)**, utiliza **MySQL** para os dados principais e **MongoDB** para o dashboard.

---

## ⚙️ Funcionalidades

- Cadastro, consulta, atualização e exclusão de **clientes**
- Cadastro, consulta, atualização e exclusão de **produtos**
- Cadastro, consulta, atualização e exclusão de **vendas**
- Dashboard com totais de clientes, produtos e vendas (**MongoDB**)
- **API RESTful** pronta para integração com front-end ou ferramentas como Postman

---

## 🛠 Tecnologias Utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- PyMySQL
- PyMongo
- MySQL
- MongoDB

---

## 📁 Estrutura do Projeto

.
├── main.py / app.py           # Arquivo principal da aplicação Flask
├── config.py                  # Configurações dos bancos de dados
├── models.py                  # Definição das tabelas (ORM)
├── sql_service.py             # Funções de manipulação SQL
├── nosql_service.py           # Funções de manipulação MongoDB
├── dashboard.py               # Blueprint do dashboard
└── requirements.txt           # Dependências do projeto

---

## 🚀 Como Executar

### 1. Pré-requisitos

- Python 3 instalado
- MySQL Server rodando e banco criado (ex: `bdpos`)
- MongoDB rodando localmente

### 2. Instale as dependências

```bash
pip install -r requirements.txt

3. Configure o banco de dados
No arquivo config.py, ajuste as conexões:

# MySQL
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:12345@127.0.0.1:3306/bdpos"

# MongoDB
MONGO_URL = "mongodb://localhost:27017"
MONGO_DB = "vendas"
MONGO_COLLECTION = "dashboard"

Obs: Crie o banco bdpos no MySQL antes de rodar o sistema:

CREATE DATABASE bdpos;

4. Execute a aplicação
python main.py

Acesse: http://localhost:5000/

🛣️ Endpoints da API
Clientes

GET /clientes — Lista todos os clientes

POST /clientes — Cria um novo cliente

GET /clientes/<id> — Consulta um cliente

PUT /clientes/<id> — Atualiza um cliente

DELETE /clientes/<id> — Remove um cliente

Produtos

GET /produtos — Lista todos os produtos

POST /produtos — Cria um novo produto

GET /produtos/<id> — Consulta um produto

PUT /produtos/<id> — Atualiza um produto

DELETE /produtos/<id> — Remove um produto

Vendas

GET /vendas — Lista todas as vendas

POST /vendas — Cria uma nova venda

GET /vendas/<id> — Consulta uma venda

PUT /vendas/<id> — Atualiza uma venda

DELETE /vendas/<id> — Remove uma venda

Dashboard

GET /dashboard/total_clientes — Total de clientes (MongoDB)

GET /dashboard/total_produtos — Total de produtos (MongoDB)

GET /dashboard/total_vendas — Total de vendas (MongoDB)

ℹ️ Observações

As tabelas são criadas automaticamente ao rodar a aplicação.

Os totais do dashboard são atualizados a cada operação de cadastro ou exclusão.

Pronto para integração com front-end ou uso via Postman.

👏 Créditos
Projeto acadêmico desenvolvido por:

Thiago Vinicius dos Santos Queiroz — RGM: 36995142

Lucas Vynicius Gonçalves Albuquerque — RGM: 39905535
