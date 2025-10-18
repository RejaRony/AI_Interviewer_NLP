# app.py (V3.1 - Production Ready)

from flask import Flask, render_template, request, jsonify, session
import traceback
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os # For the secret key

app = Flask(__name__)
# A professional application should use a secure, random secret key.
app.secret_key = os.urandom(24)

# --- SELF-HEALING STARTUP CHECK ---
# This block makes the app robust and portable. It now correctly
# checks for both 'stopwords' and 'punkt' (for tokenization).
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("NLTK data not found. Downloading necessary resources...")
    nltk.download('stopwords')
    nltk.download('punkt')
    print("Download complete.")  

# Define interview questions
interview_questions = [
    {
        'question': "Explain the difference between lists and tuples in Python.",
        'reference_answer': "Lists are mutable, meaning their elements can be changed, added, or removed after creation. Tuples are immutable; once created, their elements cannot be changed. Lists are typically used for homogenous collections where the content might change, while tuples are used for heterogeneous, fixed collections or for dictionary keys.",
        'expected_keywords': ["mutable", "immutable", "ordered", "indexable"]
    },
    {
        'question': "Describe the concept of Object-Oriented Programming (OOP).",
        'reference_answer': "OOP is a programming paradigm based on the concept of 'objects', which can contain data (attributes) and code (methods). The main pillars are Encapsulation (bundling data and methods), Inheritance (allowing new classes to reuse properties of existing ones), Polymorphism (allowing one interface to be used for a general class of actions), and Abstraction (hiding complex implementation details).",
        'expected_keywords': ["encapsulation", "inheritance", "polymorphism", "abstraction"]
    },
    {
        'question': "What is the time complexity of searching for an element in a sorted array using binary search?",
        'reference_answer': "The time complexity of binary search on a sorted array is O(log n), or logarithmic time. This is because binary search repeatedly divides the search interval in half. This makes it much faster than linear search (O(n)) for large arrays.",
        'expected_keywords': ["logarithmic", "O(log n)"]
    },
    {
        'question': "Explain the purpose of a virtual environment in Python.",
        'reference_answer': "A Python virtual environment is a self-contained directory containing a Python installation for a particular project. Its main purpose is isolation, ensuring that the packages and dependencies of one project do not conflict with those of others, which is crucial for project reproducibility and dependency management.",
        'expected_keywords': ["dependencies", "isolation", "reproducibility"]
    },
    {
        'question': "Describe the difference between TCP and UDP.",
        'reference_answer': "TCP (Transmission Control Protocol) is a connection-oriented, reliable protocol, meaning it guarantees that data is delivered in order and without errors, and requires a handshake to establish a connection. UDP (User Datagram Protocol) is a connectionless, unreliable protocol that sends data without prior setup and offers no guarantees of delivery, order, or error checking, making it faster but less secure.",
        'expected_keywords': ["connection-oriented", "connectionless", "reliable", "unreliable"]
    }
]


@app.route('/')
def index():
    try:
        session.clear()  # Start a new interview on page load
        session['question_index'] = 0
        session['score'] = 0
        # --- Start with a welcoming message and the first question ---
        initial_message = "Hello! I am your AI Interviewer. Let's begin.\n\n" + interview_questions[0]['question']
        return render_template('index.html', initial_message=initial_message)
    except Exception as e:
        print(f"Error serving index.html: {e}")
        traceback.print_exc()
        return "An error occurred while serving the page.", 500

STOPWORDS = set(stopwords.words('english'))

def preprocess_text(text):
    """Clean and tokenize text: remove special chars, punctuation, and stop words."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = text.split()
    tokens = [word for word in tokens if word not in STOPWORDS]
    return ' '.join(tokens)


def evaluate_answer(answer, reference_answer):
    """Evaluates the answer using Cosine Similarity against a reference answer."""

    # 1. Preprocess both texts
    preprocessed_answer = preprocess_text(answer)
    preprocessed_reference = preprocess_text(reference_answer)

    if not preprocessed_answer or not preprocessed_reference:
        return 0.0

    # 2. Vectorize the texts using TF-IDF
    # The TfidfVectorizer creates a numerical representation of the text
    vectorizer = TfidfVectorizer()

    # Fit and transform the texts. We pass both to ensure the vocabulary is complete.
    vectors = vectorizer.fit_transform([preprocessed_answer, preprocessed_reference])

    # 3. Calculate Cosine Similarity
    # Cosine Similarity measures the angle between the two vectors (0 to 1)
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    # Combine with simple keyword matching for robust scoring (optional but recommended)
    # Note: You can adjust the weight of the keyword score

    return similarity


@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_message = request.json['message']

        # --- Use .get() with a default for safety ---
        question_index = session.get('question_index', 0)
        score = session.get('score', 0)

        # Evaluate the user's answer to the *previous* question
        if question_index > 0 and question_index <= len(interview_questions):
            previous_question_data = interview_questions[question_index - 1]
            reference_answer = previous_question_data['reference_answer']
            answer_score = evaluate_answer(user_message, reference_answer)
            score += answer_score
            session['score'] = score

            # More dynamic feedback
            if answer_score >= 0.7:
                feedback = f"Great, that's a strong answer ({answer_score*100:.0f}% relevant). "
            elif answer_score >= 0.4:
                feedback = f"Okay, that's a good start ({answer_score*100:.0f}% relevant). "
            else:
                feedback = f"Thanks for that. Let's move on. "
        else:
            # This is the very first interaction, no previous answer to score.
            feedback = ""

        # Check if the interview is over
        if question_index < len(interview_questions):
            next_question = interview_questions[question_index]['question']
            ai_response = feedback + "Here is your next question:\n\n" + next_question
            session['question_index'] = question_index + 1
            return jsonify({'response': ai_response, 'interview_over': False})
        else:
            # End of the interview
            final_score = (score / len(interview_questions)) * 100 if interview_questions else 0
            ai_response = f"{feedback} That concludes the interview. Your final relevance score is {final_score:.0f}%. Thank you for your time."
            session.clear()
            return jsonify({'response': ai_response, 'interview_over': True})

    except Exception as e:
        print(f"Error processing message: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)