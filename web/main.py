from flask import Flask, g, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import csv
import os
import ast
import sys
import pickle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stats.train import predict_prices

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

data_folder = "./data"
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

if not os.path.exists('./web/instance/products.db'):
    with app.app_context():
        db.create_all()
        insert_data()
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
    # Open the pickle containing the summaries
    with open('./pickles/storeSummary.pkl', 'rb') as f:
        storeSummary_df = pickle.load(f)

    # Load metrics
    with open('./pickles/metrics.pkl', 'rb') as f:
        metrics = pickle.load(f)

    return render_template('statistics.html',storeSummary_df=storeSummary_df, metrics=metrics)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    store = data.get('store')
    price = float(data.get('price'))
    model_name = data.get('model')

    # Load the models from the pickle file
    with open('./pickles/models.pkl', 'rb') as f:
        models = pickle.load(f)

    # Get the unique stores from the store summary
    with open('./pickles/storeSummary.pkl', 'rb') as f:
        storeSummary_df = pickle.load(f)
    stores = storeSummary_df['store'].unique()

    # Perform the prediction
    prediction = predict_prices(store, price, models, model_name, stores)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)