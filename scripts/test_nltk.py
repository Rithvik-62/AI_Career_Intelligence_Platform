import nltk
import traceback

def test_nltk():
    try:
        nltk.data.find('corpora/stopwords')
        print("stopwords ok")
    except Exception as e:
        print("stopwords fail:", e)
        
    try:
        nltk.data.find('tokenizers/punkt')
        print("punkt ok")
    except Exception as e:
        print("punkt fail:", e)

    try:
        nltk.data.find('tokenizers/punkt_tab')
        print("punkt_tab ok")
    except Exception as e:
        print("punkt_tab fail:", e)

    try:
        nltk.data.find('corpora/wordnet')
        print("wordnet ok")
    except Exception as e:
        print("wordnet fail:", e)

if __name__ == '__main__':
    test_nltk()
