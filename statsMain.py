from stats.dataframe import createDataframe
from stats.train import create_models_metrics, predict_prices, create_classified_table
from stats.createSummaryDfs import productSummary, storeSummary
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def round_to_nearest_tens(value):
    return int(np.floor(value / 10.0) * 10)

df = createDataframe()

### "generic" graphs

stats = ["mean", "median", "std"]
stores = df['store'].unique()

# Create a color map
colors = plt.cm.tab10(range(len(stores)))

# Create summary dfs (contains descriptive statistics)
productSummary_df = productSummary(df)
storeSummary_df = storeSummary(df)

for s in stats:
    for group, group_name, summary_df in zip(['store', 'shortName'], ['Store', 'Product'], [storeSummary_df, productSummary_df]):
        plt.figure(figsize=(10, 6))

        ax = sns.barplot(x=group, y='price', data=df, estimator=s, errorbar=None)
        if s == 'mean':
            y_label = 'Average Price'
        elif s == 'median':
            y_label = 'Median Price'
        else:
            y_label = 'Standard Deviation of Price'
        
        plt.ylabel(y_label)
        plt.xlabel(group_name)

        extra_top_padding = False

        if s == 'mean' or s == 'median':
            plt.title(f'{s.capitalize()} price per {group_name}')
            min_value = round_to_nearest_tens(summary_df[f'{s}_price'].min()) - 10
            max_value = round_to_nearest_tens(summary_df[f'{s}_price'].max()) + 10
            if max_value - summary_df[f'{s}_price'].max()< 4:
                extra_top_padding = True
        else:
            plt.title(f'Standard Deviation of Price per {group_name}')
            min_value = round_to_nearest_tens(summary_df['std_dev'].min()) - 10
            max_value = round_to_nearest_tens(summary_df['std_dev'].max()) + 10
            if max_value - summary_df['std_dev'].max()< 4:
                extra_top_padding = True

        if group_name == 'Product':
            plt.xticks(rotation=90)

        if extra_top_padding and group_name == 'Product':
            max_value += 60
        
        if min_value<0:
            min_value=0
        interval = (max_value - min_value)//10
        plt.ylim(min_value, max_value)
        plt.yticks(range(min_value, max_value + interval, interval))

        if group_name == 'Store':
            for i, bar in enumerate(ax.patches):
                bar.set_color(colors[i % len(colors)])
        
        for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}',
                xy=(p.get_x() + p.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=7)
        plt.savefig(f'./stats/graphs/{group_name}/{group_name}_{s}.png', bbox_inches='tight')
        # plt.show()

####
####
# Histogram

# Prepare data for each store
price_data = [df[df['store'] == store]['price'] for store in stores]

n_bins = 8

# Plot the histograms side by side
plt.figure(figsize=(10, 6))

plt.hist(price_data, n_bins, histtype='bar', color=colors, label=stores)

# Add labels and title
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.title('Histogram of Prices by Store')

# Add legend
plt.legend(title='Store', prop={'size': 10})

plt.savefig('./stats/graphs/histogram_store.png')






# Create dataframe where each row is a product and each column is the respective price in each store
pivot_df = df.pivot(index='shortName', columns='store', values='price')
pivot_df.reset_index(inplace=True)

models, metrics = create_models_metrics(pivot_df, stores)

# Prediction usage example -> Product in Chip7 store that costs 1800
# 3 prediction models in total to try
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


###
###
# Boxplot

plt.figure(figsize=(10, 6))

# Create the boxplot
box = plt.boxplot(price_data, patch_artist=True, tick_labels=stores)

# Color the boxes
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

# Add labels and title
plt.xlabel('Store')
plt.ylabel('Price')
plt.title('Boxplot of Prices by Store')

for median in box['medians']:
    median.set_color('black')

plt.savefig('./stats/graphs/boxplot_store.png')