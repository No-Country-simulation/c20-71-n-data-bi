def engineer_features(df):
    # shift la variable objetivo
    df['Next_Day_Return'] = df['Daily_Return'].shift(-1)
    
    # Lag features: valores pasados de una variable
    lag_features = ['Close', 'EMA20', 'SMA50', 'RSI', 'OBV', 'MACD', 'Stoch_D', 'Stoch_K', 'ROC', 'Volume_SMA20']
    for feature in lag_features:
        df[f'{feature}_lag'] = df[feature].shift(1)
        
    # Agrega el dia de la semana
    df['Day_Of_week'] = df.index.dayofweek
    
    # Borra los valores nulos que se crearon
    df = df.dropna()
    return df