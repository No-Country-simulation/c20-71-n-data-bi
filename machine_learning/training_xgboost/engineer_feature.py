

def fetures_engineering(df):
    # Calculate moving averages
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    
    # Calculate price momentum
    df['momentum'] = df['close'] - df['close'].shift(5)
    
    # # Calculate volatility
    df['volatility'] = df['returns'].rolling(window=20).std()
    
    # # Calculate relative strength index (RSI)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Drop rows with NaN values
    df = df.dropna()
    
    return df