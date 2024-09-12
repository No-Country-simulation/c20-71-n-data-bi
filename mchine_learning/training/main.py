import pandas as pd
import os, sys
sys.path.append(os.getcwd)
from connection import connect_to_redshift
from data_extraction import fetch_data_from_redshift
from config import REDSHIFT_CONFIG
from preprocessing import preprocess_data
from prepare_data_for_ml import prepare_data
from model import create_and_train_model, evaluate_model

def fetch_data():
    connection = connect_to_redshift(REDSHIFT_CONFIG)
    if not connection:
        return None
    
    try:
        query = """
        SELECT * FROM eas_andes_historical_data
        """
        
        df = fetch_data_from_redshift(connection, query)
        
        return df
        
    finally:
        connection.close()
        print('Conexión finalizada')
        
def extraction_and_preprocess():
    df = fetch_data()
    if df is None:
        print('Fallo la extraccion de datos')
        return
    
    df_preprocessed = preprocess_data(df)
    print(df_preprocessed.head(5))
    
    X_train, X_test, y_train, y_test = prepare_data(df_preprocessed, 'target')
    
    return X_train, X_test, y_train, y_test
    
def model():
    
    X_train, X_test, y_train, y_test = extraction_and_preprocess()
    
    model_rfc = create_and_train_model(X_train, y_train)
    
    accuracy, report, auc_roc = evaluate_model(model_rfc, X_test, y_test)
    
    print('Accuracy:', accuracy)
    print('Report:', report)
    print('Auc_ROC:', auc_roc)
    
model()