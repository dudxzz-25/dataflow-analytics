from pathlib import Path
import random
from datetime import date, timedelta
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
random.seed(42)

customers = pd.DataFrame([
    {"customer_id": i, "name": f"Cliente {i:03d}", "city": random.choice(["São Paulo", "Campinas", "Santos", "Osasco", "Guarulhos"])}
    for i in range(1, 81)
])
products = pd.DataFrame([
    {"product_id": i, "product": f"Produto {i:02d}", "category": random.choice(["Eletrônicos", "Casa", "Esporte", "Livros"]), "unit_price": round(random.uniform(20, 900), 2)}
    for i in range(1, 31)
])

orders = []
items = []
start = date(2025, 1, 1)
for order_id in range(1, 601):
    customer_id = random.randint(1, len(customers))
    order_date = start + timedelta(days=random.randint(0, 540))
    orders.append({"order_id": order_id, "customer_id": customer_id, "order_date": order_date.isoformat(), "channel": random.choice(["Web", "App", "Loja"])})
    for line in range(random.randint(1, 4)):
        p = products.sample(1, random_state=order_id * 10 + line).iloc[0]
        qty = random.randint(1, 5)
        items.append({"order_id": order_id, "product_id": int(p.product_id), "quantity": qty, "unit_price": float(p.unit_price)})

# Deliberately add a duplicate and one missing city to demonstrate cleaning.
customers.loc[5, "city"] = None
customers = pd.concat([customers, customers.iloc[[0]]], ignore_index=True)

customers.to_csv(OUT / "customers.csv", index=False)
products.to_csv(OUT / "products.csv", index=False)
pd.DataFrame(orders).to_csv(OUT / "orders.csv", index=False)
pd.DataFrame(items).to_csv(OUT / "order_items.csv", index=False)
print(f"Dados gerados em {OUT}")
