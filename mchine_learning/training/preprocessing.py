import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    df = df.dropna()
    
    df['tomorrow'] = df['close'].shift(-1)
    
    df['target'] = (df['tomorrow'] > df['close']).astype(int)
    
    df = df.drop(['date', 'dividends', 'stock_splits', 'tomorrow'], axis=1)
    
    scaler = StandardScaler()
    
    columns = ['open', 'high', 'low', 'close', 'volume']
    df[columns] = scaler.fit_transform(df[columns])
    
    return df
    