import pandas as pd
import nltk 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib  # For saving and loading models

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt_tab')

# Load stopwords and stemmer
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()  # Lowercasing
    words = word_tokenize(text)  # Tokenizing
    # Remove stopwords and apply stemming
    filtered_words = [ps.stem(w) for w in words if w not in stop_words and w.isalpha()]
    return ' '.join(filtered_words)

# Load data
data = pd.read_csv('emailsss.csv')

# Check if model already exists
try:
    # Load the model and vectorizer
    classifier = joblib.load('spam_classifier_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    print("Model and vectorizer loaded successfully.")
    
except FileNotFoundError:
    # Model does not exist, so we need to train it

    # Apply preprocessing to the dataset
    data['cleaned_message'] = data['text'].apply(preprocess_text)

    # Feature extraction using TF-IDF
    vectorizer = TfidfVectorizer(max_features=5000)  # Limiting to 5000 features
    X = vectorizer.fit_transform(data['cleaned_message']).toarray()

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, data['spam'], test_size=0.2, random_state=42)

    # Naive Bayes classifier
    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)

    # Evaluate model
    y_pred = classifier.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Save the trained model and vectorizer
    joblib.dump(classifier, 'spam_classifier_model.pkl')
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
    print("Model and vectorizer saved.")

# Sample email to test

def classify_email(email):

# Preprocess the sample email
    cleaned_sample_email = preprocess_text(email)

# Transform the sample email using the saved TF-IDF vectorizer
    sample_email_tfidf = vectorizer.transform([cleaned_sample_email]).toarray()

# Predict if it's spam or not
    prediction = classifier.predict(sample_email_tfidf)

# Output result
    if prediction[0] == 1:
        return "spam"
    else:
        return "not spam"