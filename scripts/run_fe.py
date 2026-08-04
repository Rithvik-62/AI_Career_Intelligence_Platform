import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import json
import os

print("=== STEP 1: Load Dataset ===")
df = pd.read_csv('dataset/processed/clean_resume_dataset.csv')
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Data Types:\n{df.dtypes}")
print(f"First 5 Rows:\n{df.head()}")

assert df['Cleaned_Resume'].isnull().sum() == 0, "Missing values in Cleaned_Resume!"
assert df['mapped_category'].isnull().sum() == 0, "Missing values in mapped_category!"
print("Verified: No missing values, No duplicate records.")

print("\n=== STEP 2: Feature Selection ===")
X = df['Cleaned_Resume']
y = df['mapped_category']

print("\n=== STEP 3: Label Encoding ===")
le = LabelEncoder()
y_encoded = le.fit_transform(y)

mapping = {label: idx for idx, label in enumerate(le.classes_)}
print("Label Mapping:")
for k, v in mapping.items():
    print(f"{k} -> {v}")

os.makedirs('models', exist_ok=True)
joblib.dump(le, 'models/label_encoder.pkl')

print("\n=== STEP 4: TF-IDF Vectorization ===")
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    stop_words='english'
)

X_tfidf = vectorizer.fit_transform(X)

print(f"Vocabulary Size: {len(vectorizer.vocabulary_)}")
print(f"Feature Matrix Shape: {X_tfidf.shape}")
print(f"Sample Feature Names: {vectorizer.get_feature_names_out()[:10]}")

joblib.dump(vectorizer, 'models/vectorizer.pkl')

print("\n=== STEP 5: Train-Test Split ===")
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y_encoded, test_size=0.20, random_state=42, stratify=y_encoded
)

print(f"Training Samples: {X_train.shape[0]}")
print(f"Testing Samples: {X_test.shape[0]}")
print(f"Training Labels: {y_train.shape[0]}")
print(f"Testing Labels: {y_test.shape[0]}")

print("\n=== STEP 6: Feature Statistics ===")
num_features = X_tfidf.shape[1]
num_classes = len(le.classes_)
density = X_tfidf.nnz / (X_tfidf.shape[0] * X_tfidf.shape[1])
sparsity = 1.0 - density

print(f"Number of Features: {num_features}")
print(f"Number of Classes: {num_classes}")
print(f"Training Matrix Shape: {X_train.shape}")
print(f"Testing Matrix Shape: {X_test.shape}")
print(f"Feature Density: {density:.4f} ({density*100:.2f}%)")
print(f"Sparsity Percentage: {sparsity:.4f} ({sparsity*100:.2f}%)")

print("\n=== STEP 7: Save Processed Data ===")
joblib.dump(X_train, 'models/X_train.pkl')
joblib.dump(X_test, 'models/X_test.pkl')
joblib.dump(y_train, 'models/y_train.pkl')
joblib.dump(y_test, 'models/y_test.pkl')
print("Saved X_train, X_test, y_train, y_test to models/")

print("\n=== STEP 8: Validation ===")
assert X_train.shape[0] == y_train.shape[0]
assert X_test.shape[0] == y_test.shape[0]
assert X_train.shape[1] == X_test.shape[1]
print("Validation Passed!")

metrics = {
    "num_features": int(num_features),
    "num_classes": int(num_classes),
    "density": float(density),
    "sparsity": float(sparsity),
    "train_samples": int(X_train.shape[0]),
    "test_samples": int(X_test.shape[0]),
    "mapping": {str(k): int(v) for k, v in mapping.items()}
}
with open("fe_metrics.json", "w") as f:
    json.dump(metrics, f)
