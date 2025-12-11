#  README.md — API Gerenciadora de Carros (Flask + SQL Server / MySQL)

# API de Gerenciamento de Carros
API simples construída em **Flask**, com suporte a **SQL Server** (via ODBC) e **MySQL/MariaDB (phpMyAdmin)**.  
Permite listar, adicionar, atualizar e deletar carros.

A API envia respostas em **texto plano**, pois o front-end consome via regex.

---

##  Estrutura do Projeto

```
loja_car/
│── app.py
│── config.py
│── requirements.txt
└── .venv/
```

---

##  Instalação e Execução

### 1. Criar ambiente virtual  
Se estiver no Windows 10, use:

python -m venv .venv

Se estiver usando outro sistema operacional, consulte a documentação correspondente.

```

### 2. Ativar ambiente

**Windows PowerShell**
```bash
.venv\Scripts\Activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

Se quiser instalar manualmente:
```bash
pip install flask flask-cors pyodbc
```

---

##  Arquivo config.py

Crie o arquivo **config.py** na raiz:

###  SQL Server
```python
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=dbocarro;"
    "Trusted_Connection=yes;"
)
```

###  MySQL (phpMyAdmin / XAMPP / WAMP)
```python
CONNECTION_STRING = (
    "DRIVER={MySQL ODBC 8.0 Unicode Driver};"
    "SERVER=localhost;"
    "DATABASE=dbocarro;"
    "UID=root;"
    "PWD=;"
    "PORT=3306;"
    "charset=utf8;"
)
```

---

##  Scripts de Banco de Dados

###  SQL Server
```sql
CREATE DATABASE dbocarro;
GO

USE dbocarro;
GO

CREATE TABLE carros (
    id INT IDENTITY(1,1) PRIMARY KEY,
    modelo VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);

INSERT INTO carros (modelo, preco) VALUES
('Uno', 12000),
('Fiesta', 18000),
('Gol', 25000);
```

###  MySQL
```sql
CREATE DATABASE dbocarro;
USE dbocarro;

CREATE TABLE carros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);

INSERT INTO carros (modelo, preco) VALUES
('Uno', 12000),
('Fiesta', 18000),
('Gol', 25000);
```

---

##  Endpoints da API

###  Listar Carros  
`GET /listarCarros`

Retorno:
```
{"id":1,"modelo":"Uno","preco":12000}{"id":2,"modelo":"Fiesta","preco":18000}
```

### Adicionar Carro  
`POST /saveCarro`

Body (text/plain):
```
Modelo,Preco
```

Exemplo:
```
Fusca,15000
```

###  Atualizar Carro  
Mesma rota:
```
/saveCarro
```

###  Deletar Carro  
`POST /deleteCarro`

Body:
```
Modelo
```

Exemplo:
```
Gol
```

---

##  Funcionamento

- Respostas são texto puro (front usa regex).
- CORS ativo globalmente:
```python
CORS(app)
```
- Conexão ao banco:
```python
def get_connection():
    return pyodbc.connect(config.CONNECTION_STRING)
```

---

##  Executar a API

```bash
python app.py
```

A API sobe em:
```
http://127.0.0.1:5000
```

---

##  Dependências

Conteúdo do **requirements.txt**:
```
flask
flask-cors
pyodbc
```

---

##  Licença

Projeto liberado para estudos e uso pessoal.

---
