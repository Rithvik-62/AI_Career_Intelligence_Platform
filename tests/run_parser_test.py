import sys
import json
sys.path.append('.')
from utils.parser import ResumeParser

parser = ResumeParser()
result = parser.parse("dataset/external/sample_resume.pdf")

print("--- Parsed Result ---")
print(json.dumps(result, indent=2))

with open("parser_test_result.json", "w") as f:
    json.dump(result, f, indent=2)
