import joblib
import time
import json
import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score

def evaluate_model(model, X_train, y_train, X_test, y_test, name):
    print(f"\nEvaluating {name}...")
    start_time = time.time()
    
    # Train
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Cross Validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    
    print(f"Accuracy: {acc:.4f} | F1: {f1:.4f} | CV Mean: {cv_scores.mean():.4f}")
    
    return {
        'model': model,
        'accuracy': float(acc),
        'precision': float(prec),
        'recall': float(rec),
        'f1': float(f1),
        'cv_mean': float(cv_scores.mean()),
        'train_time': float(train_time),
        'y_pred': y_pred
    }

def main():
    os.makedirs('logs', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    print("=== STEP 1: Load Data ===")
    X_train = joblib.load('models/X_train.pkl')
    X_test = joblib.load('models/X_test.pkl')
    y_train = joblib.load('models/y_train.pkl')
    y_test = joblib.load('models/y_test.pkl')
    label_encoder = joblib.load('models/label_encoder.pkl')
    
    num_classes = len(np.unique(y_train))
    print(f"Training shape: {X_train.shape}")
    print(f"Testing shape: {X_test.shape}")
    print(f"Number of classes: {num_classes}")
    
    models = {
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5, weights='uniform'),
        'SVM': SVC(kernel='linear', probability=True, random_state=42)
    }
    
    results = {}
    best_model_name = None
    best_score = -1
    
    for name, model in models.items():
        res = evaluate_model(model, X_train, y_train, X_test, y_test, name)
        results[name] = res
        
        # We will use accuracy or f1 to select the best model. Using accuracy.
        if res['accuracy'] > best_score:
            best_score = res['accuracy']
            best_model_name = name

    print(f"\n=== STEP 2: Selected Best Model: {best_model_name} (Acc: {best_score:.4f}) ===")
    
    # Save best model
    best_model = results[best_model_name]['model']
    joblib.dump(best_model, 'models/career_model.pkl')
    print("Saved best model to models/career_model.pkl")
    
    # Save the individual models just in case (optional, but good for backup)
    joblib.dump(results['Decision Tree']['model'], 'models/decision_tree_model.pkl')
    joblib.dump(results['KNN']['model'], 'models/knn_model.pkl')
    joblib.dump(results['SVM']['model'], 'models/svm_model.pkl')
    
    # Generate Reports for best model
    y_pred = results[best_model_name]['y_pred']
    cm = confusion_matrix(y_test, y_pred).tolist()
    cr = classification_report(y_test, y_pred, target_names=label_encoder.classes_, zero_division=0)
    
    print("\nClassification Report (Best Model):")
    print(cr)
    
    summary = {
        "best_model": best_model_name,
        "metrics": {
            name: {k: v for k, v in res.items() if k not in ['model', 'y_pred']} 
            for name, res in results.items()
        },
        "confusion_matrix": cm,
        "classification_report": classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True, zero_division=0)
    }
    
    with open("logs/model_comparison.json", "w") as f:
        json.dump(summary, f, indent=4)
        
    print("Training pipeline finished. Reports saved to logs/")

if __name__ == "__main__":
    main()
