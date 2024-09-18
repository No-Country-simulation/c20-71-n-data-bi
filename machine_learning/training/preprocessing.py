import pandas as pd

def preprocess_data(df):
    
    df_featured = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    
    df_featured['date'] = pd.to_datetime(df_featured['date'])
    df_featured = df_featured.drop_duplicates()
    df_featured = df_featured.set_index('date')
    #df_featured = df_featured.sort_index()
    
    df_featured['tomorrow'] = df_featured['close'].shift(-1)
    
    df_featured['target'] = (df_featured['tomorrow'] > df_featured['close']).astype(int)
    
    df_featured['month'] = df_featured.index.month
    df_featured['day_of_week'] = df_featured.index.dayofweek
    
    # Calculate daily returns
    df_featured['returns'] = df_featured['close'].pct_change()
    
    print(df_featured.head(5))
    
    return df_featured
    