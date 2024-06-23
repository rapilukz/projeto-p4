def productSummary(df):
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
    return productSummary_df

def storeSummary(df):
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
    return storeSummary_df