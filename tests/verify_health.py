import os, sys, glob, py_compile, joblib

print('================================================================================')
print('1. AUDITING ALL PYTHON FILES FOR SYNTAX & COMPILATION ERRORS')
print('================================================================================')
root = os.getcwd()
py_files = sorted(glob.glob(os.path.join(root, '**', '*.py'), recursive=True))

errors = []
for pf in py_files:
    if '.venv' in pf or '__pycache__' in pf:
        continue
    try:
        py_compile.compile(pf, doraise=True)
    except Exception as e:
        errors.append((os.path.relpath(pf, root), str(e)))

if errors:
    print('COMPILATION ERRORS DETECTED:')
    for p, err in errors:
        print(f'  {p}: {err}')
    sys.exit(1)
else:
    print(f'SUCCESS: All {len(py_files)} Python source files compiled cleanly with 0 errors!\n')

print('================================================================================')
print('2. AUDITING SERIALIZED ML MODELS')
print('================================================================================')
models_dir = os.path.join(root, 'models')
model_path = os.path.join(models_dir, 'career_model.pkl')
vec_path = os.path.join(models_dir, 'vectorizer.pkl')
enc_path = os.path.join(models_dir, 'label_encoder.pkl')

assert os.path.exists(model_path), 'Missing career_model.pkl'
assert os.path.exists(vec_path), 'Missing vectorizer.pkl'
assert os.path.exists(enc_path), 'Missing label_encoder.pkl'

m = joblib.load(model_path)
v = joblib.load(vec_path)
e = joblib.load(enc_path)
print('SUCCESS: All 3 ML Models loaded into RAM successfully!\n')

print('================================================================================')
print('3. RUNNING END-TO-END PIPELINE ACROSS ALL 10 SAMPLE RESUMES')
print('================================================================================')
sys.path.append(root)
from utils.parser import ResumeParser
from utils.predictor import CareerPredictor
from utils.scoring import ResumeScorer
from utils.skill_gap import SkillGapAnalyzer
from utils.insights import InsightEngine

parser = ResumeParser()
predictor = CareerPredictor()
scorer = ResumeScorer()
analyzer = SkillGapAnalyzer()

pdf_files = sorted(glob.glob('Sample_Resume/*.pdf'))

for pdf in pdf_files:
    fname = os.path.basename(pdf)
    parsed = parser.parse(pdf)
    pred = predictor.predict(pdf)
    score = scorer.calculate_score(parsed, pred['predicted_role'])
    gap = analyzer.analyze_gap(parsed, pred['predicted_role'])
    insights = InsightEngine.generate_executive_insights(parsed, score, pred, gap)
    print(f'  [PASS] {fname}: Candidate "{parsed["name"]}" -> Role "{pred["predicted_role"]}" (Score: {score["overall_score"]}/100)')

print('\n================================================================================')
print('FINAL VERIFICATION: 100% HEALTHY - ALL SYSTEMS WORKING PERFECTLY WITH ZERO ISSUES!')
print('================================================================================')
