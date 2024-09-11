import pandas as pd
import os, sys
sys.path.append(os.getcwd)
from connection import connect_to_redshift
from data_extraction import fetch_data_from_redshift
from config import REDSHIFT_CONFIG
from preprocessing import preprocess_data
from prepare_data_for_ml import prepare_data

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
        
def extraction():
    df = fetch_data()
    if df is None:
        print('Fallo la extraccion de datos')
        return
    
    df_preprocessed = preprocess_data(df)
    print(df_preprocessed.head(5))
    
    X_train, X_target, y_test, y_target = prepare_data(df_preprocessed, 'target')
    
    print(X_train.shape)
    print(X_target.shape)
    print(y_test.shape)
    print(y_target.shape)
    
extraction()