from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
import csv
import json
import os
import ast

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
    
    def get_reviews_list(self):
        try:
            return ast.literal_eval(self.reviews)
        except ValueError:
            return []

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
            reviews = row['reviews']
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
        insert_data()
        db.create_all()
        print("Database created")

## Start of the web application
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    reviews_list = Product.get_reviews_list(product)
    return render_template('product_details.html', product=product, reviews=reviews_list)

@app.route('/graphs')
def graph():
    return render_template('graphs.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

if __name__ == '__main__':
    app.run(debug=True)