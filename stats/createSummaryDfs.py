import pickle

def productSummary(df):
    product_summary_path = './pickles/productSummary.pkl'
    productSummary_df = df.groupby('shortName').agg(
        mean_price=('price', 'mean'),
        median_price=('price', 'median'),
        Q1=('price', lambda x: x.quantile(0.25)),
        Q3=('price', lambda x: x.quantile(0.75)),
        variance=('price', 'var'),
        std_dev=('price', 'std'),
        min_price=('price', 'min'),
        max_price=('price', 'max')
    ).reset_index()

    with open(product_summary_path, 'wb') as f:
        pickle.dump(productSummary_df, f)
    
    print(f"Product summary saved to {product_summary_path}")

def storeSummary(df):
    store_summary_path = './pickles/storeSummary.pkl'
    storeSummary_df = df.groupby('store').agg(
        mean_price=('price', 'mean'),
        median_price=('price', 'median'),
        Q1=('price', lambda x: x.quantile(0.25)),
        Q3=('price', lambda x: x.quantile(0.75)),
        variance=('price', 'var'),
        std_dev=('price', 'std'),
        min_price=('price', 'min'),
        max_price=('price', 'max')
    ).reset_index()

    with open(store_summary_path, 'wb') as f:
        pickle.dump(storeSummary_df, f)
    
    print(f"Store summary saved to {store_summary_path}")
