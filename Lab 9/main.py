from tasks.tokenization import run_tokenization
from tasks.stopwords import run_stopwords
from tasks.sentiment import run_sentiment

with open("data/sample.txt", "r") as f:
    text = f.read().strip()

print("=" * 50)
print("Input Text:", text)
print("=" * 50)

run_tokenization(text)
run_stopwords(text)
run_sentiment(text)
