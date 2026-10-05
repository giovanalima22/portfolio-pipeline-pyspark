from pathlib import Path
import random
from datetime import date, timedelta
import pandas as pd

random.seed(7)
OUT = Path("data/raw")
OUT.mkdir(parents=True, exist_ok=True)

products = [
    (101, "Notebook Pro", "Eletrônicos", 4200),
    (102, "Monitor 24", "Eletrônicos", 950),
    (103, "Teclado Mecânico", "Periféricos", 420),
    (104, "Mouse Sem Fio", "Periféricos", 180),
    (105, "Headset", "Periféricos", 310),
]

rows = []
start = date(2026, 1, 1)

for i in range(1, 1001):
    d = start + timedelta(days=random.randint(0, 180))
    pid, name, category, price = random.choice(products)
    rows.append({
        "order_id": i,
        "order_date": d.isoformat(),
        "customer_id": random.randint(1, 200),
        "product_id": pid,
        "product_name": name,
        "category": category,
        "quantity": random.randint(1, 5),
        "unit_price": price,
        "status": random.choice(["PAID", "PAID", "PAID", "CANCELLED"]),
    })

df = pd.DataFrame(rows)
df.to_csv(OUT / "orders.csv", index=False)
print(f"Generated {len(df)} records.")
