import pandas as pd
import numpy as np

np.random.seed(42)

# Config
num_rows = 5000

products = [
    ("Laptop", "Electronics", 800, 500),
    ("Phone", "Electronics", 600, 350),
    ("Shoes", "Clothing", 120, 60),
    ("Jacket", "Clothing", 200, 100),
    ("Blender", "Home", 150, 90),
    ("Bike", "Sports", 500, 300),
    ("Watch", "Accessories", 250, 80),
]

regions = ["North America", "Europe", "Asia"]
segments = ["Retail", "Online", "Wholesale"]

dates = pd.date_range(start="2023-01-01", end="2025-12-31")

data = []

for i in range(num_rows):
    product = products[np.random.randint(len(products))]
    date = np.random.choice(dates)

    quantity = np.random.randint(1, 5)

    # Add some randomness to price
    price = product[2] * np.random.uniform(0.9, 1.1)
    cost = product[3] * np.random.uniform(0.9, 1.1)

    data.append([
        i,
        date,
        product[0],
        product[1],
        np.random.choice(regions),
        np.random.choice(segments),
        quantity,
        round(price, 2),
        round(cost, 2)
    ])

df = pd.DataFrame(data, columns=[
    "transaction_id",
    "order_date",
    "product_name",
    "category",
    "region",
    "customer_segment",
    "quantity",
    "unit_price",
    "unit_variable_cost"
])

df.to_csv("sales_data.csv", index=False)

print("Dataset generated!")