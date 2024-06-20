from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
import csv
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

data_folder = "../data"
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shortName = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    store = db.Column(db.String, nullable=False)
    ratings = db.Column(db.Float, nullable=False)
    reviews = db.Column(db.Text, nullable=False)
    reviews_nr = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Product {self.id}>'

def convert_to_int(value):
    try:
        return int(value.replace(',', ''))
    except ValueError:
        return 0 #  Default value if conversion fails

def convert_to_float(value):
    try:
        return float(value.replace(',', ''))
    except ValueError:
        return 0.0  # Default value if conversion fails

def insert_data_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reviews = json.dumps(row['reviews'].split('|')) #  Convert reviews to JSON string
            product = Product(
                shortName=row['shortName'],
                name=row['name'],
                category=row['category'],
                price=convert_to_float(row['price']),
                store=row['store'],
                ratings=convert_to_float(row['ratings']),
                reviews=reviews,
                reviews_nr=convert_to_int(row['reviews_nr'])
            )
            db.session.add(product)

    db.session.commit()


def insert_data():
    for file in os.listdir(data_folder):
        if file.endswith('.csv'):
            insert_data_from_csv(os.path.join(data_folder, file))

    print("Data insertion complete.")


if not os.path.exists('./instance/products.db'):
    with app.app_context():
        db.create_all()
        insert_data()
        print("Database created")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)