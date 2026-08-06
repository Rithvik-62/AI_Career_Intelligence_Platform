import pandas as pd

df = pd.read_csv('dataset/raw/resume_dataset.csv')
print('Shape:', df.shape)
print('Columns:', df.columns.tolist())
print()

print('--- FIRST 5 RESUME TEXTS (FULL) ---')
for i in range(5):
    role = df['Role'].iloc[i]
    text = df['Resume_Text'].iloc[i]
    print(f'Row {i} | Role: {role}')
    print(f'Text: {text[:400]}')
    print()

print('--- CHECKING IF DATASET IS SYNTHETIC ---')
# Check if resume texts are template-like / repetitive
sample_texts = df['Resume_Text'].dropna().head(20).tolist()
for i, t in enumerate(sample_texts[:5]):
    print(f"Text {i}: {t[:150]}")
    print()

# Check unique text patterns
print("First words of each resume:")
for i in range(10):
    t = str(df['Resume_Text'].iloc[i])
    print(f"  Row {i}: {t[:80]}")
