# DataFlow Analytics

[![CI](https://github.com/dudxzz-25/dataflow-analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/dudxzz-25/dataflow-analytics/actions/workflows/ci.yml)

Pipeline ETL de vendas construído com **Python, Pandas e SQL**. O projeto simula uma pequena operação comercial, trata dados brutos, aplica validações de qualidade, carrega um banco SQLite e disponibiliza consultas analíticas para exploração.

## 🎯 Objetivo

Demonstrar um fluxo de dados reproduzível:

```text
CSV bruto → validação e limpeza → transformação → SQLite → consultas analíticas
```

## 🛠️ Stack

**Python · Pandas · SQLite · SQL · unittest**

## ✅ O que o projeto demonstra

- limpeza de dados ausentes e duplicados;
- normalização de datas e valores monetários;
- validação de chaves e integridade referencial;
- criação de schema relacional e índices;
- carga transacional em banco SQL;
- geração de métricas de faturamento, ticket médio, clientes e produtos;
- testes automatizados do fluxo de transformação e carga.

## 📂 Estrutura

```text
dataflow-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   └── generate_data.py
├── sql/
│   └── analytics.sql
├── src/
│   └── etl.py
├── tests/
│   └── test_etl.py
├── requirements.txt
└── README.md
```

## ▶️ Como executar

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_data.py
python src/etl.py
```

O banco é criado em `data/processed/dataflow.db` e os CSVs tratados ficam em `data/processed/`.

### Consultas analíticas

```bash
sqlite3 data/processed/dataflow.db < sql/analytics.sql
```

### Testes

```bash
python -m unittest discover -s tests -v
```

## 🧠 Decisões técnicas

- chaves inválidas são filtradas antes da carga para preservar integridade referencial;
- itens repetidos dentro do mesmo pedido são agregados antes da persistência;
- o pipeline gera saídas intermediárias em CSV para facilitar auditoria e inspeção;
- os dados do projeto são sintéticos e voltados exclusivamente a estudo e portfólio.

---

Desenvolvido por **Eduardo de Toledo Dias**.

[Portfólio](https://dudxzz-25.github.io/portfolio-web/) · [GitHub](https://github.com/dudxzz-25) · [LinkedIn](https://www.linkedin.com/in/eduardo-de-toledo-dias-880b9834b/)