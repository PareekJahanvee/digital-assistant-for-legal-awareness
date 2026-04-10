import csv
import nltk
import os
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from chatbot_db import init_chatbot_db, save_conversation

# NLTK setup
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# 🔹 Preprocess text
def preprocess(text):
    words = word_tokenize(text.lower())
    cleaned = [
        lemmatizer.lemmatize(word)
        for word in words
        if word.isalnum() and word not in stop_words
    ]
    return " ".join(cleaned)

# 🔹 Load dataset
def load_legal_data(csv_path='dataset.csv'):
    questions = []
    answers = []
    topics = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = row.get('Question', '').strip()
            a = row.get('Answer', '').strip()
            t = row.get('Topic', '').strip()

            if q and a:
                questions.append(preprocess(q))
                answers.append(a)
                topics.append(t)

    print(f" Loaded {len(questions)} rows")
    return questions, answers, topics

# 🔹 Initialize data
questions, answers, topics = load_legal_data()

vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

# 🔹 Main chatbot function
def get_best_answer(user_question):
    user_vec = vectorizer.transform([preprocess(user_question)])
    similarities = cosine_similarity(user_vec, question_vectors)[0]

    top_indices = similarities.argsort()[-5:][::-1]

    best_idx = top_indices[0]
    best_score = similarities[best_idx]

    query_lower = user_question.lower()

    for idx in top_indices:
        topic_lower = topics[idx].lower()
        if any(word in topic_lower for word in query_lower.split()):
            best_idx = idx
            best_score = similarities[idx]
            break

    if best_score < 0.25:
        response = (
            "Sorry, I couldn't find a confident answer. "
            "Try being more specific (e.g. 'fundamental rights in India', 'how to file FIR')."
        )
        save_conversation(user_question, response)
        return response

    confidence = round(best_score * 100, 2)
    answer = answers[best_idx]
    topic = topics[best_idx]

    response = f"{answer}\n\n📌 Topic: {topic}\n(Confidence: {confidence}%)"

    save_conversation(user_question, response)

    return response

# 🔹 Initialize DB (important)
init_chatbot_db()