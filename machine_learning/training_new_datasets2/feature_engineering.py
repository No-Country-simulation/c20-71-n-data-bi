# Función para crear nuevas características
def engineer_features(df):
    # shift la variable objetivo
    df['Next_Day_Close'] = df['Close'].shift(-1)
    
    df['Target'] = (df['Next_Day_Close'] >= 0).astype(int)
    
    # Lag features (Características de desfase): valores pasados de una variable
    lag_features = ['EMA20', 'SMA50', 'OBV', 'Stoch_D', 'Stoch_K', 'ROC', 'Volume_SMA20', 'Daily_Return']
    for feature in lag_features:
        df[f'{feature}_Lag1'] = df[feature].shift(1)
        df[f'{feature}_Lag2'] = df[feature].shift(2)
    
    # # Media movil
    # for feature in lag_features:
    #     df[f'{feature}_rolling_mean'] = df[feature].shift().rolling(10).mean()
    
    # Agrega el dia de la semana
    df['Day_Of_week'] = df.index.dayofweek
    
    # # Se borran columnas más irrelevantes para el modelo
    # df = df.drop(['Year', 'Stoch_D', 'RSI', 'Day', 'Month', 'Stoch_K'], axis=1)
    
    # Borra los valores nulos que se crearon
    df = df.dropna()
    return df