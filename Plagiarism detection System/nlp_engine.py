import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_dataset(path):
    """Load dataset safely with debug."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        content = content.replace('\r\n', '\n').replace('\r', '\n')

        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', content) if p.strip()]

        if len(paragraphs) <= 1:
            lines = [line.strip() for line in content.splitlines() if len(line.strip()) > 5]
            if lines:
                return lines

        return paragraphs if paragraphs else []

    except Exception as e:
        print(" Dataset loading error:", e)
        return []


def calculate_similarity(user_text, documents):
    if not documents:
        return 0.0, "No dataset found", []

    if not user_text or not user_text.strip():
        return 0.0, "No input provided", []

    all_texts = documents + [user_text]

    try:
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True
        )
        vectors = vectorizer.fit_transform(all_texts)
    except Exception as e:
        print("Vectorizer error:", e)
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(all_texts)

    similarity_scores = cosine_similarity(vectors[-1], vectors[:-1])

    max_index = int(similarity_scores.argmax())
    max_score = float(similarity_scores[0][max_index]) * 100

    matched_doc = documents[max_index]
    plagiarized_words = get_common_words(user_text, matched_doc)

    return max_score, matched_doc, plagiarized_words


def get_common_words(text1, text2):
    def tokenize(text):
        return set(re.findall(r'\b[a-zA-Z]{3,}\b', text.lower()))

    words1 = tokenize(text1)
    words2 = tokenize(text2)

    return list(words1 & words2)