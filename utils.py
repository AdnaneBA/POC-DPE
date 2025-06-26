import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import psycopg2
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from typing import List, Optional, Dict, Any
from collections import defaultdict

def train_predict_from_user_input(df: pd.DataFrame, user_input: Optional[Dict[str, Any]] = None):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    import seaborn as sns

    target_col = 'etiquette_dpe'

    # 1. On enlève la target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 2. On restreint aux colonnes renseignées par l'utilisateur
    used_features = list(user_input.keys())
    X = X[used_features]

    # 3. Encodage du X complet (train)
    qualitative_cols = X.select_dtypes(include=['object', 'category']).columns
    X_encoded = pd.get_dummies(X, columns=qualitative_cols, drop_first=True)

    # 4. Split
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # 5. Entraînement du modèle
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # 6. Score de test
    acc = rf.score(X_test, y_test)
    print(f"✅ Test Accuracy: {acc:.2f}")

    # 7. Encodage des données utilisateur
    user_df = pd.DataFrame([user_input])
    user_encoded = pd.get_dummies(user_df)

    # 🔥 ALIGNEMENT ici — c’est crucial
    user_encoded = user_encoded.reindex(columns=X_encoded.columns, fill_value=0)

    # 8. Prédiction
    prediction = rf.predict(user_encoded)[0]
    print(f"🔮 Prédiction sur données utilisateur : {prediction}")

    # 9. Affichage des 20 variables les plus importantes
    importances = rf.feature_importances_
    feature_names = X_encoded.columns
    feature_importance = pd.Series(importances, index=feature_names).sort_values(ascending=False)

    # plt.figure(figsize=(10, 6))
    # sns.barplot(x=feature_importance[:20], y=feature_importance.index[:20])
    # plt.title("Top 20 Features Importantes")
    # plt.xlabel("Importance")
    # plt.tight_layout()
    # plt.show()

    return prediction, acc

from sklearn.preprocessing import LabelEncoder

def train_predict_from_user_input_xgboost(df: pd.DataFrame, user_input: Optional[Dict[str, Any]] = None):
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    from xgboost import XGBClassifier
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    import seaborn as sns

    target_col = 'etiquette_dpe'

    # 1. Séparer X et y
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 🔤 Encodage de y
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)  # 'A' -> 0, ..., 'G' -> 6

    # 2. Utiliser uniquement les colonnes fournies par l'utilisateur
    used_features = list(user_input.keys())
    X = X[used_features]

    # 3. Encodage de X (variables catégorielles)
    qualitative_cols = X.select_dtypes(include=['object', 'category']).columns
    X_encoded = pd.get_dummies(X, columns=qualitative_cols, drop_first=True)
    X_encoded.columns = X_encoded.columns.str.replace(r"[<>[\]()]","_", regex=True)
    # 4. Split
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

    # 5. Entraînement du modèle
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    xgb.fit(X_train, y_train)

    # 6. Score
    acc = xgb.score(X_test, y_test)
    print(f"✅ Test Accuracy (XGBoost): {acc:.2f}")



    # 7. Traitement de l'entrée utilisateur
    user_df = pd.DataFrame([user_input])
    user_encoded = pd.get_dummies(user_df)
    user_encoded.columns = user_encoded.columns.str.replace(r"[<>[\]()]","_", regex=True)
    user_encoded = user_encoded.reindex(columns=X_encoded.columns, fill_value=0)

    # 8. Prédiction
    prediction_num = xgb.predict(user_encoded)[0]
    prediction_label = le.inverse_transform([prediction_num])[0]  # Reconvertir vers A-G
    print(f"🔮 Prédiction sur données utilisateur : {prediction_label}")

    # 9. Features importantes
    importances = xgb.feature_importances_
    feature_names = X_encoded.columns
    feature_importance = pd.Series(importances, index=feature_names).sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importance[:20], y=feature_importance.index[:20])
    plt.title("Top 20 Features Importantes (XGBoost)")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.show()

        # Prédictions sur le test set
    y_pred_test = xgb.predict(X_test)

    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred_test)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)

    # Affichage
    plt.figure(figsize=(8, 6))
    disp.plot(cmap="Blues", values_format="d")
    plt.title("Confusion Matrix (XGBoost)")
    plt.grid(False)
    plt.show()

    return prediction_label, acc