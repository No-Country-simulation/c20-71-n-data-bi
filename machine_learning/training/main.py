import pandas as pd
import os, sys
sys.path.append(os.getcwd)
from connection import connect_to_redshift
from data_extraction import fetch_data_from_redshift
from config import REDSHIFT_CONFIG
from preprocessing import preprocess_data
from engineer_feature import fetures_engineering
from model import train_model, evaluate_model, make_prediction

def model(company_name):
    
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
    
    prediction = 'Up' if prediction[0] == 1 else 'Down'
    
    description = 'Probabilidad de que suba' if prediction[0] == 1 else 'Probabilidad de que baje'
    
    return prediction, description


comercial_name = ['YPF Sociedad Anonima (YPF)',
                  'Pampa Energía S.A. (PAM)',
                  'Ecopetrol S.A. (EC)',
                  'Petróleo Brasileiro S.A. - Petrobras (PBR)',
                  'Interconexión Eléctrica S.A. E.S.P. (IESFY)',
                  'Centrais Elétricas Brasileiras S.A. - Eletrobrás (EBR)',
                  'Engie Brasil Energia S.A. (EGIE3.SA)',
                  'Vista Energy, S.A.B. de C.V. (VIST)',
                  'Atlas Energy Solutions Inc. (AESI)',
                  'Compañía de Minas Buenaventura S.A.A. (BVN)'
                  ]

company_name = ['ypf', 'pampa_energía', 'ecopetrol', 'petrobras', 'interconexion_electrica', 'eletrobras', 'engie_brasil_energia',
'vista_energy', 'eas_andes', 'minas_buenaventura']

predictions = []
descriptions = []

for company in company_name:
    prediction, description = model(company)
    if prediction is None:
        sys.exit(1)
    
    predictions.append(prediction)
    descriptions.append(description) 

my_dict = {'Nombre de la empresa':comercial_name,
           'Predicción':predictions,
           'Descripción':description
           }

print(len(predictions))
print(len(descriptions))
my_df = pd.DataFrame(my_dict)
my_df.to_csv('predicciones/predicciones.csv')