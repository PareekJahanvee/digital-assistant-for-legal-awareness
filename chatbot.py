from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import csv
from .chatbot_db import init_chatbot_db, save_conversation, view_conversations

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text):
    words = word_tokenize(text.lower())
    cleaned_words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word.isalnum() and word not in stop_words
    ]
    return " ".join(cleaned_words)

# ====================== LOAD CSV DATA ======================
def load_legal_data(csv_path='dataset.csv'):
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            questions = []
            answers = []
            
            for row in reader:
                q_text = row.get('Question', '').strip()
                a_text = row.get('Answer', '').strip()
                
                if q_text and a_text:
                    questions.append(preprocess(q_text))
                    answers.append(a_text)
            
            print(f"✅ Successfully loaded {len(questions):,} question-answer pairs from dataset.csv")
            return questions, answers

    except FileNotFoundError:
        print("❌ dataset.csv not found! Please keep it in the same folder as chatbot.py")
        raise
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        raise

# Load the big dataset
questions, answers = load_legal_data()

# Train TF-IDF on all 5000+ questions
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

def get_best_answer(user_question):
    user_vector = vectorizer.transform([preprocess(user_question)])
    similarities = cosine_similarity(user_vector, question_vectors)
    
    best_match_index = similarities.argmax()
    best_score = similarities[0][best_match_index]

    if best_score < 0.30:   # Slightly lowered threshold for large dataset
        return (
            "I'm sorry, I couldn't find a confident match for your question.\n\n"
            "Try rephrasing or ask about:\n"
            "- FIR, Arrest Rights, Bail\n"
            "- Fundamental Rights & Writs\n"
            "- Courts & Judiciary\n"
            "- Consumer Rights, Property, Marriage"
        )

    confidence = round(best_score * 100, 2)
    return f"{answers[best_match_index]}\n\n(Confidence: {confidence}%)"

# ====================== DATABASE SETUP ======================
init_chatbot_db()
# view_conversations()   # Uncomment if you want to see history on startup

print("\n🚀 Legal AI Chatbot Ready!")
print("   Powered by 5000+ legal Q&A from dataset.csv")
print("   Type 'exit' to quit\n")