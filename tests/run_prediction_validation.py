import pandas as pd
import numpy as np
import json
import os
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import time

sys.path.append('.') # To allow importing utils
from utils.predictor import CareerPredictor

def create_pdf(text, filepath):
    c = canvas.Canvas(filepath, pagesize=letter)
    textobject = c.beginText()
    textobject.setTextOrigin(50, 750)
    textobject.setFont("Helvetica", 10)
    
    # Wrap text to fit in PDF
    words = text.split()
    line = ""
    for word in words:
        if len(line) + len(word) > 100:
            textobject.textLine(line)
            line = word + " "
        else:
            line += word + " "
    textobject.textLine(line)
    
    c.drawText(textobject)
    c.save()

def main():
    print("=== STARTING PREDICTION VALIDATION ===")
    
    df = pd.read_csv('dataset/processed/clean_resume_dataset.csv')
    
    # Sample 3 resumes per class if possible, else all
    samples = []
    classes = df['mapped_category'].unique()
    for cls in classes:
        cls_df = df[df['mapped_category'] == cls]
        n_samples = min(3, len(cls_df))
        samples.append(cls_df.sample(n_samples, random_state=42))
        
    test_df = pd.concat(samples).reset_index(drop=True)
    
    os.makedirs('temp_pdfs', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    predictor = CareerPredictor()
    
    results = []
    correct_count = 0
    total_confidence = 0
    misclassified = []
    
    for idx, row in test_df.iterrows():
        expected_career = row['mapped_category']
        resume_text = row['resume_text']
        
        pdf_path = f"temp_pdfs/resume_{idx}.pdf"
        create_pdf(resume_text, pdf_path)
        
        # Predict
        res = predictor.predict(pdf_path)
        
        if "error" in res:
            print(f"Error predicting resume {idx}: {res['error']}")
            continue
            
        predicted_career = res['predicted_role']
        confidence = res['confidence']
        top_3 = res['top_predictions']
        
        is_correct = expected_career == predicted_career
        if is_correct:
            correct_count += 1
        else:
            misclassified.append({
                "resume_id": idx,
                "expected": expected_career,
                "predicted": predicted_career,
                "confidence": confidence
            })
            
        total_confidence += confidence
        
        results.append({
            "resume_id": idx,
            "expected": expected_career,
            "predicted": predicted_career,
            "confidence": confidence,
            "top_3": top_3,
            "correct": is_correct
        })
        
        print(f"ID: {idx} | Expected: {expected_career} | Predicted: {predicted_career} | Conf: {confidence}% | Correct: {is_correct}")

    total_tested = len(results)
    overall_accuracy = correct_count / total_tested if total_tested > 0 else 0
    avg_confidence = total_confidence / total_tested if total_tested > 0 else 0
    
    print(f"\n=== VALIDATION SUMMARY ===")
    print(f"Total Tested: {total_tested}")
    print(f"Overall Accuracy: {overall_accuracy * 100:.2f}%")
    print(f"Average Confidence: {avg_confidence:.2f}%")
    print(f"Misclassified Count: {len(misclassified)}")
    
    # Per-class accuracy
    print("\n--- Per-Class Accuracy ---")
    class_stats = {}
    for res in results:
        exp = res['expected']
        if exp not in class_stats:
            class_stats[exp] = {"total": 0, "correct": 0}
        class_stats[exp]["total"] += 1
        if res["correct"]:
            class_stats[exp]["correct"] += 1
            
    for cls, stats in class_stats.items():
        acc = stats["correct"] / stats["total"]
        print(f"{cls}: {acc*100:.2f}% ({stats['correct']}/{stats['total']})")
        
    validation_report = {
        "overall_accuracy": float(overall_accuracy),
        "average_confidence": float(avg_confidence),
        "total_tested": int(total_tested),
        "per_class_accuracy": {cls: stats["correct"] / stats["total"] for cls, stats in class_stats.items()},
        "misclassified": misclassified,
        "detailed_results": results
    }
    
    with open("logs/validation_report.json", "w") as f:
        json.dump(validation_report, f, indent=4)
        
    print("\nValidation report saved to logs/validation_report.json")

if __name__ == "__main__":
    main()
