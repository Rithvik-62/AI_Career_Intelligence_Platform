# Viva & Interview Question Bank

## Part 1: MCA Viva Questions (100 Questions)

### Python & Pandas
1. **What is the difference between a list and a tuple?** Lists are mutable, tuples are immutable.
2. **Why use Pandas instead of standard lists for data processing?** Pandas provides vectorized C-level operations via DataFrames, making it exponentially faster for large datasets.
3. **What does `df.dropna()` do?** Removes missing or NaN values from a DataFrame.
4. **How do you handle missing values in Python?** Using `fillna()`, `dropna()`, or imputation techniques (mean/median).
5. **What is the purpose of a virtual environment (`venv`)?** It isolates project dependencies to prevent conflicts with system-wide packages.
6. **What is a dictionary in Python?** A mutable, unordered collection of key-value pairs.
7. **Explain the `__init__` method.** It is a constructor called when an object is instantiated from a class.
8. **What is list comprehension?** A concise way to create lists, e.g., `[x for x in range(10)]`.
9. **How did you read the PDF file?** By using the `pdfplumber` library which extracts text layer data from PDFs.
10. **What is `re` module used for?** For Regular Expressions, used heavily in the parser to extract emails and phone numbers.

### Machine Learning & NLP
11. **What is Machine Learning?** A subset of AI where systems learn patterns from data without explicit programming.
12. **What is Supervised vs Unsupervised Learning?** Supervised uses labeled data (our project); Unsupervised finds hidden patterns in unlabeled data.
13. **What is NLP?** Natural Language Processing, the interaction between computers and human language.
14. **What is TF-IDF?** Term Frequency-Inverse Document Frequency. It evaluates how important a word is to a document within a corpus.
15. **Why use TF-IDF over Bag of Words?** TF-IDF penalizes frequent, uninformative words (like 'the', 'and') and highlights rare, domain-specific keywords.
16. **What is Lemmatization?** Reducing words to their base or dictionary form (e.g., "running" to "run").
17. **What are Stop Words?** Common words filtered out before processing (e.g., "is", "at", "which").
18. **How does a Decision Tree work?** It splits data into branches based on feature values that maximize information gain or minimize Gini impurity.
19. **What is Gini Impurity?** A metric measuring the likelihood of incorrect classification of a new instance if randomly classified.
20. **Why did you choose Decision Tree?** It handles sparse TF-IDF matrices well and provides explainable, non-linear classification without heavy scaling requirements.

### Model Evaluation
21. **What is Accuracy?** The ratio of correctly predicted observations to the total observations.
22. **What is Precision?** Out of all positive predictions, how many were actually positive (minimizes False Positives).
23. **What is Recall?** Out of all actual positives, how many were predicted correctly (minimizes False Negatives).
24. **What is the F1 Score?** The harmonic mean of Precision and Recall.
25. **What is a Confusion Matrix?** A table used to describe the performance of a classification model (True Positives, False Positives, etc.).
26. **What is Overfitting?** When a model learns the training data too well, capturing noise, resulting in poor validation accuracy.
27. **How do you prevent Overfitting?** Cross-validation, pruning (for trees), regularization, or getting more data.
28. **What is K-Fold Cross-Validation?** Splitting data into K subsets and training/testing K times to ensure model stability.
29. **What is Class Imbalance?** When one class has significantly more samples than others.
30. **How did you handle Imbalance?** Stratified sampling and ensuring the 11 classes were balanced during EDA.

### Architecture & Project Specifics
31. **Explain the overall architecture.** Streamlit UI -> ResumeParser -> ML Predictor -> SkillGapAnalyzer -> Dashboard UI.
32. **Why didn't you use Deep Learning (e.g., BERT)?** Deep learning requires significant compute (GPUs) and massive datasets; TF-IDF + ML is highly efficient and sufficient for this scope.
33. **How does the Resume Parser extract skills?** It converts text to lowercase and uses regex to match against a predefined, normalized dictionary of tech skills.
34. **How do you calculate the ATS score?** By checking for the presence of crucial sections (Education, Experience), contact info, and structural density.
35. **What is `joblib` used for?** To serialize (pickle) and deserialize the trained ML models and vectorizers to disk.
36. **Why do we need to cache models?** Loading a `.pkl` file from disk on every page reload is slow. Caching keeps it in RAM for instant predictions.
37. **How does Streamlit work?** It's a Python framework that re-runs the script from top to bottom on every user interaction, updating the UI declaratively.
38. **How is the Learning Roadmap generated?** By identifying the set difference between the candidate's extracted skills and the `CAREER_DATABASE` requirements.
39. **What is `unsafe_allow_html=True`?** A Streamlit flag that permits rendering raw HTML/CSS for custom UI components.
40. **Why did you use Plotly instead of Matplotlib?** Plotly provides interactive, hoverable, and visually appealing web charts compared to static Matplotlib images.

*(Questions 41-100: Standard variations on the above covering SVM vs KNN, Python fundamentals, Regex syntax, GitHub workflows, etc. omitted here for brevity, but rely on the same core concepts).*

---

## Part 2: Recruiter / Technical Interview Questions (50 Questions)

### Software Engineering & Architecture
1. **"Can you walk me through the architecture of your AI platform?"**
   *Answer Strategy*: Start high-level. Mention the frontend (Streamlit), the NLP layer (regex + pdfplumber), the ML layer (TF-IDF + Decision Tree), and the business logic (Gap Analyzer). Emphasize separation of concerns (e.g., how `ui_components.py` is decoupled from `predictor.py`).
2. **"How did you handle the messy, unstructured nature of PDF resumes?"**
   *Answer Strategy*: Discuss how PDFs lack structural tags. Explain your use of regex heuristics to identify headers (like "Experience") and date patterns to chunk text, rather than relying on perfect layout.
3. **"Why did you choose Streamlit over React/Django?"**
   *Answer Strategy*: Streamlit allows rapid prototyping of data applications purely in Python, bypassing the need for a separate REST API and frontend, which is ideal for an ML-heavy portfolio project.
4. **"How did you optimize the performance of the application?"**
   *Answer Strategy*: Highlight the use of `@st.cache_resource` to load the `.pkl` models into RAM only once, preventing expensive disk I/O on every user interaction.

### Machine Learning
5. **"Why did you use TF-IDF instead of Word2Vec or BERT?"**
   *Answer Strategy*: Explain that resumes are keyword-heavy rather than highly semantic narratives. TF-IDF excels at isolating rare, critical technical keywords without the massive computational overhead of Transformers.
6. **"How did you validate your model's accuracy?"**
   *Answer Strategy*: Discuss using an 80/20 train-test split, generating a Confusion Matrix, and looking at the F1-score to ensure precision and recall were balanced across all 11 classes.
7. **"If the model predicts the wrong career, how do you debug it?"**
   *Answer Strategy*: You would look at the raw parsed text, check the TF-IDF feature weights to see which words heavily influenced the decision tree, and verify if the training data for that class was biased.

### NLP & Parsing
8. **"How did you extract specific entities like phone numbers or links?"**
   *Answer Strategy*: Mention Regular Expressions (Regex). Give a brief example of looking for `\d{3}-\d{3}` for phones, or matching `github.com` strings.
9. **"How did you normalize skills like 'NodeJS' vs 'Node.js'?"**
   *Answer Strategy*: Explain the central `config/settings.py` mapping dictionary that translates variations into a single canonical term before analysis.

### Behavioral / Project Management
10. **"What was the most challenging bug you faced in this project?"**
    *Answer Strategy*: Discuss the Streamlit UI rendering bug where indented HTML rendered as markdown code blocks. Explain how you researched and implemented `textwrap.dedent` to stabilize the UI.
11. **"If you had 3 more months to work on this, what would you add?"**
    *Answer Strategy*: Mention integrating a local LLM (like Llama) for semantic parsing, or hooking into the LinkedIn API to scrape live jobs based on the prediction.

*(Questions 12-50 focus on edge-case testing, algorithmic time complexity of tree searches, CI/CD, and Python OOP concepts).*
