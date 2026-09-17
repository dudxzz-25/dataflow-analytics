# DataFlow Analytics

Pipeline ETL de vendas construído com **Python, Pandas e SQL**. O projeto gera dados brutos, executa limpeza e validações, carrega um banco SQLite e produz consultas analíticas prontas para exploração.

## Stack
- Python 3.10+
- Pandas
- SQLite / SQL

## Arquitetura
`CSV bruto -> validação/limpeza -> transformação -> SQLite -> consultas analíticas`

## Como executar
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_data.py
python src/etl.py
```

O banco será criado em `data/processed/dataflow.db` e os dados limpos em `data/processed/`.

## Consultas
```bash
sqlite3 data/processed/dataflow.db < sql/analytics.sql
```

## Testes
```bash
python -m unittest discover -s tests -v
```

## Principais entregas
- limpeza de dados ausentes e duplicados;
- normalização de datas e valores monetários;
- validação de integridade referencial;
- carga transacional em banco SQL;
- métricas de faturamento, ticket médio, clientes e produtos.
