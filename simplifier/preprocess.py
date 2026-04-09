import re
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab')

# 1. Clean raw text
def clean_text(text):
    # Normalize whitespace
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)

    # Remove headers/footers or multiple dots
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'IN THE [A-Z ]+ COURT.*?(?=[A-Z])', '', text)
    text = re.sub(r'COPY OF .*REGISTERED.*MARKS.*', '', text)

    # Normalize quotes and punctuation
    text = re.sub(r'[“”‘’]', '"', text)
    text = re.sub(r'[^A-Za-z0-9.,;:!?\'"()\-\/ ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# 2. Split into sentences
def split_into_sentences(text):
    sentences = sent_tokenize(text)
    return sentences

# 3. Chunking
def chunk_text(sentences, max_words=400):
    chunks = []
    current_chunk = []
    current_length = 0
    for sent in sentences:
        words = len(sent.split())
        if current_length + words <= max_words:
            current_chunk.append(sent)
            current_length += words
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sent]
            current_length = words
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def preprocess_text(text):
    cleaned = clean_text(text)
    print("CLEANED TEXT:\n", cleaned)

    sentences = split_into_sentences(cleaned)
    chunks = chunk_text(sentences)

    print("\nCHUNKS READY FOR SUMMARIZATION:\n")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: {chunk}\n")

    return cleaned, chunks
