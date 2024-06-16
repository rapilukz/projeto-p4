from stats.dataframe import createDataframe
from stats.train import create_models_metrics, predict_prices, create_classified_table
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = createDataframe()

# TODO more "generic" graphs
##
##

# Get unique stores
stores = df['store'].unique()

# Create dataframe where each row is a product and each column is the respective price in each store
pivot_df = df.pivot(index='shortName', columns='store', values='price')
pivot_df.reset_index(inplace=True)

models, metrics = create_models_metrics(pivot_df, stores)

prices = predict_prices("Chip7", 1800, models,"Linear Regression", stores)

classified_table = create_classified_table(pivot_df, stores, 0.15)

# print(classified_table)
# print(prices)

plt.figure(figsize=(12,6))
sns.countplot(data=classified_table, x='Store', hue='Classification', palette='viridis')
plt.title('Product Classification in Different Stores')
plt.xlabel('Store')
plt.ylabel('Count')
plt.legend(title='Classification')
plt.savefig('./stats/graphs/productClassification.png')

df_heatmap = classified_table.pivot_table(index='shortName', columns='Store', values='Classification', aggfunc='first')

classification_dict = {'Cheap': 0, 'Medium': 1, 'Expensive': 2}
df_heatmap_encoded = df_heatmap.replace(classification_dict)

plt.figure(figsize=(18, 10))
sns.heatmap(df_heatmap_encoded, annot=df_heatmap, fmt='', cmap='viridis', cbar=False)
plt.title('Product Classification Heatmap')
plt.xlabel('Store')
plt.ylabel('Product')
plt.savefig('./stats/graphs/classificationHeatmap.png')