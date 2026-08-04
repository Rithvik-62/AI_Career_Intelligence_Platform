import pandas as pd
import numpy as np
import joblib
import time
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import shutil

artifact_dir = r"C:\Users\RITHVIK\.gemini\antigravity-ide\brain\8275ec1b-0877-4169-9623-09c354bcea30"
os.makedirs(artifact_dir, exist_ok=True)
plt.style.use('ggplot')

# Step 1: Load Models & Data
X_train = joblib.load('models/X_train.pkl')
y_train = joblib.load('models/y_train.pkl')
X_test = joblib.load('models/X_test.pkl')
y_test = joblib.load('models/y_test.pkl')
label_encoder = joblib.load('models/label_encoder.pkl')

dt_model = joblib.load('models/decision_tree_model.pkl')
knn_model = joblib.load('models/knn_model.pkl')
svm_model = joblib.load('models/svm_model.pkl')

class_names = label_encoder.classes_

models = {
    'Decision Tree': dt_model,
    'KNN': knn_model,
    'SVM': svm_model
}

# Training times from phase 5 manually injected or approximated since we didn't save them. 
# We'll just approximate for the table or measure inference time. The prompt says "Training Time" for the table, 
# I will just write dummy values or refit them briefly just to get the time.
# Let's refit quickly to get training time to be accurate for the table
training_times = {}
print("Refitting models to capture precise training times...")
for name, model in models.items():
    start = time.time()
    model.fit(X_train, y_train)
    training_times[name] = time.time() - start

metrics_data = []

# Generate Predictions & Metrics
for name, model in models.items():
    print(f"\n--- Evaluating {name} ---")
    preds = model.predict(X_test)
    
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, average='weighted', zero_division=0)
    rec = recall_score(y_test, preds, average='weighted', zero_division=0)
    f1 = f1_score(y_test, preds, average='weighted', zero_division=0)
    
    print("Classification Report:")
    report = classification_report(y_test, preds, target_names=class_names)
    print(report)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, preds)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title(f'Confusion Matrix: {name}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig(os.path.join(artifact_dir, f'cm_{name.replace(" ", "_").lower()}.png'))
    plt.close()
    
    # Cross Validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy', n_jobs=-1)
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()
    print(f"5-Fold CV Mean Accuracy: {cv_mean:.4f} (+/- {cv_std:.4f})")
    
    metrics_data.append({
        'Model': name,
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1': f1,
        'Cross Validation Mean': cv_mean,
        'Training Time': training_times[name]
    })

df_metrics = pd.DataFrame(metrics_data)
print("\n=== Model Comparison Table ===")
print(df_metrics.to_string(index=False))

# Visualizations
metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1', 'Cross Validation Mean']
for metric in metrics_to_plot:
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Model', y=metric, data=df_metrics, palette='viridis')
    plt.title(f'{metric} Comparison')
    plt.ylim(0, 1.1)
    for i, v in enumerate(df_metrics[metric]):
        plt.text(i, v + 0.02, f"{v:.4f}", ha='center')
    plt.tight_layout()
    plt.savefig(os.path.join(artifact_dir, f'compare_{metric.replace(" ", "_").lower()}.png'))
    plt.close()

# Best Model Selection
best_model_row = df_metrics.sort_values(by=['Cross Validation Mean', 'Accuracy', 'F1'], ascending=[False, False, False]).iloc[0]
best_model_name = best_model_row['Model']
print(f"\nBest Model Selected: {best_model_name}")

if best_model_name == 'Decision Tree':
    shutil.copy('models/decision_tree_model.pkl', 'models/career_model.pkl')
elif best_model_name == 'KNN':
    shutil.copy('models/knn_model.pkl', 'models/career_model.pkl')
else:
    shutil.copy('models/svm_model.pkl', 'models/career_model.pkl')

print("Verified models/career_model.pkl exists:", os.path.exists('models/career_model.pkl'))

with open("eval_results.json", "w") as f:
    json.dump({"best_model": best_model_name, "metrics": df_metrics.to_dict(orient="records")}, f)
