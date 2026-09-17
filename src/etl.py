from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
DB_PATH = PROCESSED / "dataflow.db"
PROCESSED.mkdir(parents=True, exist_ok=True)


def load_raw(raw_dir: Path = RAW):
    files = {
        "customers": "customers.csv",
        "products": "products.csv",
        "orders": "orders.csv",
        "order_items": "order_items.csv",
    }
    return {name: pd.read_csv(raw_dir / filename) for name, filename in files.items()}


def transform(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    customers = tables["customers"].drop_duplicates("customer_id").copy()
    customers["city"] = customers["city"].fillna("Não informado").str.strip()
    customers["name"] = customers["name"].str.strip()

    products = tables["products"].drop_duplicates("product_id").copy()
    products["unit_price"] = pd.to_numeric(products["unit_price"], errors="coerce")
    products = products[products["unit_price"].gt(0)]

    orders = tables["orders"].drop_duplicates("order_id").copy()
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders = orders.dropna(subset=["order_date"])
    orders["order_date"] = orders["order_date"].dt.strftime("%Y-%m-%d")
    orders = orders[orders["customer_id"].isin(customers["customer_id"])]

    items = tables["order_items"].copy()
    for col in ["quantity", "unit_price"]:
        items[col] = pd.to_numeric(items[col], errors="coerce")
    items = items.dropna(subset=["quantity", "unit_price"])
    items = items[(items["quantity"] > 0) & (items["unit_price"] > 0)]
    items = items[
        items["order_id"].isin(orders["order_id"]) &
        items["product_id"].isin(products["product_id"])
    ]
    items["line_total"] = (items["quantity"] * items["unit_price"]).round(2)

    return {"customers": customers, "products": products, "orders": orders, "order_items": items}


def create_schema(conn: sqlite3.Connection):
    conn.executescript("""
    PRAGMA foreign_keys = ON;
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    );
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product TEXT NOT NULL,
        category TEXT NOT NULL,
        unit_price REAL NOT NULL CHECK(unit_price > 0)
    );
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
        order_date TEXT NOT NULL,
        channel TEXT NOT NULL
    );
    CREATE TABLE order_items (
        order_id INTEGER NOT NULL REFERENCES orders(order_id),
        product_id INTEGER NOT NULL REFERENCES products(product_id),
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        unit_price REAL NOT NULL CHECK(unit_price > 0),
        line_total REAL NOT NULL,
        PRIMARY KEY(order_id, product_id)
    );
    CREATE INDEX idx_orders_customer ON orders(customer_id);
    CREATE INDEX idx_orders_date ON orders(order_date);
    """)


def save(tables: dict[str, pd.DataFrame], db_path: Path = DB_PATH):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        create_schema(conn)
        # Respect FK dependency order.
        tables["customers"].to_sql("customers", conn, if_exists="append", index=False)
        tables["products"].to_sql("products", conn, if_exists="append", index=False)
        tables["orders"].to_sql("orders", conn, if_exists="append", index=False)
        # Duplicate product in same order can exist in source; aggregate first.
        items = (tables["order_items"]
                 .groupby(["order_id", "product_id"], as_index=False)
                 .agg(quantity=("quantity", "sum"), unit_price=("unit_price", "mean")))
        items["line_total"] = (items.quantity * items.unit_price).round(2)
        items.to_sql("order_items", conn, if_exists="append", index=False)


def main():
    raw = load_raw()
    clean = transform(raw)
    for name, df in clean.items():
        df.to_csv(PROCESSED / f"{name}_clean.csv", index=False)
    save(clean)
    print(f"ETL concluído. Banco: {DB_PATH}")
    print("Linhas carregadas:", {k: len(v) for k, v in clean.items()})


if __name__ == "__main__":
    main()
