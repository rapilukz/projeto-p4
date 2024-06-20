import sqlite3
import os
import json
import csv
from utils.functions import convert_to_float, convert_to_int

# Connect to SQLite database
conn = sqlite3.connect('products.db')

# Create a cursor object
cursor = conn.cursor()

# SQL command to create products table
create_table_command = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shortName TEXT,
    name TEXT,
    category TEXT,
    price REAL,
    store TEXT,
    ratings REAL,
    reviews TEXT,
    reviews_nr INTEGER
);
"""
data_folder = "../data"

def insert_data_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert reviews to JSON string
            reviews = json.dumps(row['reviews'].split('|'))  # Assuming reviews are pipe-separated in the CSV
            product_data = (
                row['shortName'],
                row['name'],
                row['category'],
                convert_to_float(row['price']),
                row['store'],
                convert_to_float(row['ratings']),
                reviews,
                convert_to_int(row['reviews_nr'])  # Convert reviews_nr to integer
            )
            insert_product_command = """
            INSERT INTO products (shortName, name, category, price, store, ratings, reviews, reviews_nr)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_product_command, product_data)

    # Commit the changes
    conn.commit()

conn.execute(create_table_command)
for file in os.listdir(data_folder):
    if file.endswith('.csv'):
        insert_data_from_csv(os.path.join(data_folder, file))


# Commit the changes
conn.commit()

# Close the connection
conn.close()
