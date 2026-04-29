from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
 
def run_stopwords(text):
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
 
    words = word_tokenize(text)
    stop_words = stopwords.words('english')
 
    filtered = [w for w in words if w.lower() not in stop_words]
 
    print("Original Words:", words)
    print("Filtered Words (no stopwords):", filtered)
    print("Words Removed:", len(words) - len(filtered))