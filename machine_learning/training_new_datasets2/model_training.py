import pandas as pd
from sklearn.model_selection import train_test_split, TimeSeriesSplit, RandomizedSearchCV
# from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
# from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from scipy.stats import uniform, randint

# Función para separar caracterísitcas y objetivo
def prepare_data(df):
    X = df.drop(['Daily_Return', 'Next_Day_Return', 'Target'], axis=1)
    y = df['Target']
    return train_test_split(X, y, test_size=0.2, shuffle=False)

def tune_hyperparameters(X_train, y_train):
    param_distributions = {
        'n_estimators': randint(100, 1000),
        'learning_rate': uniform(0.01, 0.3),
        'max_depth': randint(3, 10),
        'min_child_weight': randint(1, 10),
        'subsample': uniform(0.7, 0.3),
        'colsample_bytree': uniform(0.7, 0.3)
    }

    model = xgb.XGBClassifier(random_state=42)
    
    # Use TimeSeriesSplit for cross-validation
    tscv = TimeSeriesSplit(n_splits=5)

    random_search = RandomizedSearchCV(
        estimator=model, 
        param_distributions=param_distributions, 
        n_iter=50,  # Number of parameter settings that are sampled
        cv=tscv,
        n_jobs=-1,
        verbose=2, 
        scoring='roc_auc',
        random_state=42
    )

    random_search.fit(X_train, y_train)

    print("Best parameters found: ", random_search.best_params_)
    print("Best score: ", random_search.best_score_)

    return random_search.best_estimator_

# Función para entrenar y evaluar el modelo
def train_and_evaluate(X_train, X_test, y_train, y_test):
    # Scaler para estandarizar las caracteristicas
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entrenamiento del maodelo
    #model = RandomForestRegressor(n_estimators=200, max_depth=10, min_samples_leaf=5, min_samples_split=5, random_state=42)
    best_model = tune_hyperparameters(X_train_scaled, y_train)
    best_model.fit(X_train_scaled, y_train)

    # Predicción
    y_pred = best_model.predict(X_test_scaled)

    # Error cuadrático medio y valor r2
    accuracy = accuracy_score(y_test, y_pred)
    auc_roc = roc_auc_score(y_test, y_pred)
    reporte = classification_report(y_test, y_pred)
    
    print('Reporte:', reporte)

    return best_model, scaler, accuracy, auc_roc

# Función para realiza un validación cruzada para series temporales
def perform_cv(X, y):
    # Se usa TimeSeriesSplit para crear 5 validaciones cruzadas
    tscv = TimeSeriesSplit(n_splits=5)
    
    # Lista vacía para guardar los valores de r2 de cada modelo de la validación cruzada
    cv_scores = []

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    best_model = tune_hyperparameters(X_scaled, y)
    
    # Ciclo para guardar los valores r2 para cada split
    for train_index, val_index in tscv.split(X):
        # Divide las características y el objetivo en entrenamiento y validación
        X_train_cv, X_val_cv = X.iloc[train_index], X.iloc[val_index]
        y_train_cv, y_val_cv = y.iloc[train_index], y.iloc[val_index]
        
        # Escala las características
        X_train_cv_scaled = scaler.transform(X_train_cv)
        X_val_cv_scaled = scaler.transform(X_val_cv)
        
        # Entrena el modelo
        #model = RandomForestRegressor(n_estimators=100, random_state=42)
        model = xgb.XGBClassifier(**best_model.get_params())
        model.fit(X_train_cv_scaled, y_train_cv)
        y_pred_cv = model.predict(X_val_cv_scaled)
        
        # Guarda los valores r2 del modelo de cada split
        cv_scores.append(accuracy_score(y_val_cv, y_pred_cv))

    return cv_scores

# Función para predecir el valor del día siguiente
def predict_next_day(model, scaler, X):
    # Toma el último valor de las características
    last_data_point = X.iloc[-1].values.reshape(1, -1)
    # Escala este último valor usando el mismo escalador
    last_data_point_scaled = scaler.transform(last_data_point)
    # retorna el valor predicho
    return model.predict(last_data_point_scaled)[0]

# Función para determinar la importancia de cada característica en el entrenamiento de cada modelo
def get_feature_importance(model, X):
    return pd.DataFrame({'feature': X.columns, 'importance': model.feature_importances_})