import sys
import tempfile
from pathlib import Path
import sqlite3
import unittest
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.etl import transform, save

class TestETL(unittest.TestCase):
    def test_transform_and_save(self):
        raw = {
            "customers": pd.DataFrame([[1," Ana ",None],[1," Ana ","SP"]], columns=["customer_id","name","city"]),
            "products": pd.DataFrame([[1,"P","Cat",10.0]], columns=["product_id","product","category","unit_price"]),
            "orders": pd.DataFrame([[1,1,"2026-01-01","Web"]], columns=["order_id","customer_id","order_date","channel"]),
            "order_items": pd.DataFrame([[1,1,2,10.0]], columns=["order_id","product_id","quantity","unit_price"]),
        }
        clean = transform(raw)
        self.assertEqual(len(clean["customers"]), 1)
        self.assertEqual(clean["customers"].iloc[0]["city"], "Não informado")
        self.assertEqual(clean["order_items"].iloc[0]["line_total"], 20.0)
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "x.db"
            save(clean, db)
            with sqlite3.connect(db) as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 1)

if __name__ == "__main__":
    unittest.main()
