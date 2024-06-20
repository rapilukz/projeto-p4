import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor

from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score


def create_models_metrics(df, stores):
    # Train a model for each store using the other stores' prices as features
    models = {"Linear Regression":{}, "Decision Trees":{}, "Neural Network":{}}
    metrics = {"Linear Regression":{}, "Decision Trees":{}, "Neural Network":{}}
    for store in stores:
        print(f"Training the model for {store}")
        X = df[[store]]  # Use Amazon prices as input feature
        y = df.drop(columns=[store, 'shortName'])  # Prices of other stores as output
        # print(f"x:\n",X)
        # print(f"y:\n",y)

        #Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # print(y_test)
        
        # Train the model
        model1 = LinearRegression()
        model1.fit(X_train.values, y_train)

        model2 = DecisionTreeRegressor()
        model2.fit(X_train.values, y_train)

        model3 = MLPRegressor(hidden_layer_sizes=(80,80), max_iter=1100)
        model3.fit(X_train.values, y_train)
        
        # Store the model
        models["Linear Regression"][store] = model1
        models["Decision Trees"][store] = model2
        models["Neural Network"][store] = model3

        for r in list(metrics.keys()):
            metrics[r][store] = {}
            y_pred = models[r][store].predict(X_test.values)
            metrics[r][store]["mae"] = mean_absolute_error(y_test, y_pred)
            metrics[r][store]["mse"] = root_mean_squared_error(y_test, y_pred)
            metrics[r][store]["r_2"] = r2_score(y_test, y_pred)
    
    return models, metrics

def predict_prices(store, price, models, modelType, stores):

    # Create a dictionary to store the known price and predicted prices
    prices = {store: price}
    index = np.where(stores == store)[0][0]
    # print(index)
    newStores = np.delete(stores, index)

    model = models[modelType][store]
    predicted_prices = model.predict([[price]])
    # print(predicted_prices)
    
    for i, s in enumerate(newStores):
        prices[s] = predicted_prices[0][i]
    
    return prices

def classify_price(row, store):
    if row[store] < row['Lower_Threshold']:
        return "Cheap"
    elif row[store] > row['Upper_Threshold']:
        return "Expensive"
    else:
        return "Medium"

def create_classified_table(df, stores, threshold):
    df['Average'] = df[stores].mean(axis=1)

    df['Lower_Threshold'] = df['Average'] * (1-threshold)
    df['Upper_Threshold'] = df['Average'] * (1+threshold)

    for store in stores:
        df[store + "_class"] = df.apply(lambda row: classify_price(row, store), axis=1)

    df_melted = df.melt(id_vars=['shortName'], value_vars=['Amazon_class', 'Chip7_class', 'Nanochip_class', 'PC Componentes_class', 'PC Diga_class', 'Worten_class'],
                         var_name='Store', value_name='Classification')
    df_melted['Store'] = df_melted['Store'].str.replace('_class','')

    return df_melted
