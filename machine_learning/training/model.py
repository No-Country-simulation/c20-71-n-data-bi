import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def train_model(X, y):
    
    class_weights = dict(zip(np.unique(y), 1 / np.bincount(y) * len(y) / 2))
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=25, shuffle=False)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_leaf=2, min_samples_split=50, class_weight=class_weights,
                                   random_state=25)
    model.fit(X_train_scaled, y_train)
    
    return model, scaler, X_test_scaled, y_test

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    auc_roc = roc_auc_score(y_test, y_pred)
    return accuracy, report, auc_roc

def make_prediction(model, scaler, latest_data):
    latest_data_scaled = scaler.transform(latest_data)
    
    prediction = model.predict(latest_data_scaled)
    
    return prediction