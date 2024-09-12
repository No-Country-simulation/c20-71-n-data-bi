from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

def create_and_train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=2, min_samples_split=2, random_state=25)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    auc_roc = roc_auc_score(y_test, y_pred)
    return accuracy, report, auc_roc