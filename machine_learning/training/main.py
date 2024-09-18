import pandas as pd
import os, sys
sys.path.append(os.getcwd)
#import joblib
from connection import connect_to_redshift
from data_extraction import fetch_data_from_redshift
from config import REDSHIFT_CONFIG
from preprocessing import preprocess_data
from engineer_feature import fetures_engineering
from model import train_model, evaluate_model, make_prediction

def main(company_name):
    
    connection = connect_to_redshift(REDSHIFT_CONFIG)
    if not connection:
        print('No se pudo conectar a la base de datos')
        return None
    
    try:
        query = f"""
        SELECT * FROM {company_name}_historical_data
        """
        
        df = fetch_data_from_redshift(connection, query)
        
    finally:
        connection.close()
        print('Conexión finalizada')
        
        
    if df is None:
        print('Fallo la extraccion de datos')
        return None
        
    print(df.head(5))
    
    df = preprocess_data(df)
    
    df = fetures_engineering(df)
    
    print(df.head(5))
    
    X = df.drop(['target', 'tomorrow'], axis=1)
    y = df['target']
    
    model, scaler, X_test, y_test = train_model(X, y)
    
    accuracy, report, auc_roc = evaluate_model(model, X_test, y_test)
    
    print('Accuracy del modelo:', accuracy)
    print('Reoporte:')
    print(report)
    print('Valor AUC-ROC:', auc_roc)
    
    latest_data = X.iloc[-1].values.reshape(1,-1)
    prediction = make_prediction(model, scaler, latest_data)
    
    print(f"Prediction for next day: {'Up' if prediction[0] == 1 else 'Down'}")

if __name__ == "__main__":
    
    company_name = 'ypf'
    result = main(company_name)
    if result is None:
        sys.exit(1)
    
#joblib.dump(model_rfc, f'machine_learning/model/model_rfc_{company_name}.joblib')