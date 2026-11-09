# D&D 5e Parallel REST API ETL — Python & PostgreSQL

Pipeline de Engenharia de Dados em **Python** para extração concorrente de dados da **D&D 5e REST API** (`https://www.dnd5eapi.co`), normalização de payloads JSON e carga em lote (*batch insert*) em banco de dados relacional **PostgreSQL** (`psycopg2`).

---

## Arquitetura do Pipeline (ETL)

1. **Extract (Extração Concorrente com Reaproveitamento de Sessão HTTP):**
   - Utiliza `requests.Session()` para manter o *connection pooling* (TCP Keep-Alive) durante a coleta de centenas de endpoints de detalhes (`/api/monsters/{index}`).
   - Paraleliza as requisições HTTP com `concurrent.futures.ThreadPoolExecutor(max_workers=5)`, reduzindo drasticamente o tempo de I/O de rede em comparação à coleta sequencial (`consulta_gemini.py` vs. `consulta_paralela.py`).
2. **Transform (Normalização e Tratamento Resiliente de Payloads):**
   - Extrai e padroniza os atributos essenciais de cada entidade (`nome`, `tipo`, `nivel_desafio` / CR e `hp`), tratando exceções por requisição e aplicando *fallbacks* seguros.
3. **Load (Persistência Relacional em PostgreSQL):**
   - Gerencia conexões parametrizadas via variáveis de ambiente (`python-dotenv`) e executa inserções unitárias ou em lote (`cursor.executemany`) na tabela `monstros_dnd` via `psycopg2`.

---

## Stack Tecnológica

- **Linguagem:** Python 3.12+
- **Concorrência & Rede:** `requests` (`requests.Session`), `concurrent.futures` (`ThreadPoolExecutor`)
- **Banco de Dados & Configuração:** **PostgreSQL**, `psycopg2-binary`, `python-dotenv`

---

## Estrutura do Projeto

```text
├── consulta_generica/
│   ├── main.py                # Orquestrador do pipeline (Extração -> Carga -> Consulta)
│   ├── consulta_paralela.py   # Extração multithread com ThreadPoolExecutor e requests.Session
│   ├── consulta_gemini.py     # Protótipo sequencial com slicing para validação rápida de payload
│   ├── db.py                  # Camada de persistência PostgreSQL (connect, executemany, select)
│   └── teste_revisao.py       # Script de validação de conectividade HTTP
├── schema.sql                 # DDL de criação da tabela no PostgreSQL
├── .env.example               # Template de variáveis de ambiente para conexão ao banco
└── requirements.txt           # Dependências do projeto
```

---

## Como Executar

```bash
# 1. Criar ambiente virtual e instalar dependências
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
copy .env.example .env
# Edite o arquivo .env com as credenciais do seu PostgreSQL local e execute o schema.sql

# 3. Executar o pipeline
python consulta_generica/main.py
```
