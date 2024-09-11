from sklearn.model_selection import train_test_split

def prepare_data(df, target):
    X = df.drop(target, axis=1)
    y = df[target]
    
    X_train, X_target, y_test, y_target = train_test_split(X, y, test_size=0.2, random_state=25)
    
    return X_train, X_target, y_test, y_target