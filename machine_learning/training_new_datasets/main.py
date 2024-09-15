import os, sys
sys.path.append(os.getcwd)
import numpy as np
from data_loader import load_data
from feature_engineering import engineer_features
from model_training import prepare_data, train_and_evaluate, perform_cv, predict_next_day, get_feature_importance

def main():
    # Carga los datos y los preprocesa
    df = load_data('datasets_modelo/3r_petroleum_model_data.csv')
    df = engineer_features(df)

    # Preparación para el entrenamiento del modelo
    X_train, X_test, y_train, y_test = prepare_data(df)

    # Entrena y evalua el modelo
    model, scaler, rmse, r2 = train_and_evaluate(X_train, X_test, y_train, y_test)
    print(f'Error cuadrático medio (RMSE): {rmse}')
    print(f'Valor R2: {r2}')

    # Realiza la validación cruzada
    cv_scores = perform_cv(X_train, y_train)
    print(f'Valores R2 de la validación cruzada: {cv_scores}')
    print(f'Media de los valores R2 {np.mean(cv_scores)}')

    # Predicción d valor del día siguiente
    next_day_prediction = predict_next_day(model, scaler, X_test)
    print(f'Predicted return for the next day: {next_day_prediction}')

    # Se obtiene las características más importantes durante la evaluación
    feature_importance = get_feature_importance(model, X_test)
    print(feature_importance.sort_values('importance', ascending=False))

if __name__ == "__main__":
    main()