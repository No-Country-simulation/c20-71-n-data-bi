from sklearn.model_selection import train_test_split

def prepare_data(df, target):
    X = df.drop(target, axis=1)
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=25, shuffle=False)
    
    return X_train, X_test, y_train, y_test