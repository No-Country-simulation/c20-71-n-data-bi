import pandas as pd
import os, sys
sys.path.append(os.getcwd)
import joblib
from connection import connect_to_redshift
from data_extraction import fetch_data_from_redshift
from training.config import REDSHIFT_CONFIG
#from preprocessing import preprocess_data
#from prepare_data_for_ml import prepare_data
#from model import create_and_train_model, evaluate_model

def fetch_data(company_name):
    connection = connect_to_redshift(REDSHIFT_CONFIG)
    if not connection:
        return None
    
    try:
        query = f"""
        SELECT * FROM {company_name}_historical_data
        """
        
        df = fetch_data_from_redshift(connection, query)
        
        return df
        
    finally:
        connection.close()
        print('Conexión finalizada')
        
def extraction_and_preprocess(company_name):
    df = fetch_data(company_name)
    if df is None:
        print('Fallo la extraccion de datos')
        return
    
    # df_preprocessed = preprocess_data(df)
    # print(df_preprocessed.head(5))
    
    # X_train, X_test, y_train, y_test = prepare_data(df_preprocessed, 'target')
    
    return df
    
# def model(company_name):
    
#     X_train, X_test, y_train, y_test = extraction_and_preprocess(company_name)
    
#     model_rfc = create_and_train_model(X_train, y_train)
    
#     accuracy, report, auc_roc = evaluate_model(model_rfc, X_test, y_test)
    
#     print('Accuracy:', accuracy)
#     print('Report:', report)
#     print('Auc_ROC:', auc_roc)
    
#     return model_rfc

# company_name = 'ypf'
# model_rfc = model(company_name)

joblib.dump(model_rfc, f'machine_learning/model/model_rfc_{company_name}.joblib')