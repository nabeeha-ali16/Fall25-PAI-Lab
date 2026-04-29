from textblob import TextBlob
 
def run_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
 
    print("Sentiment:", blob.sentiment)
 
    if polarity > 0:
        label = "Positive"
    elif polarity < 0:
        label = "Negative"
    else:
        label = "Neutral"
 
    print("Polarity Score :", round(polarity, 2), "→", label)
    print("Subjectivity   :", round(subjectivity, 2), "(0 = Objective, 1 = Subjective)")
 
    