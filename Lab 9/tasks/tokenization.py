from nltk.tokenize import word_tokenize
import nltk
 
def run_tokenization(text):
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
 
    tokens = word_tokenize(text)
    print("Tokens:", tokens)
    print("Total Tokens:", len(tokens))
 