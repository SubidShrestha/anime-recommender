import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import scipy.sparse as sp
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import joblib
import nltk

# Download the stopwords from NLTK
nltk.download('stopwords')
nltk.download('punkt')

df = pd.read_csv('anime.csv')
# Preprocess data
def preprocess_text(text):
    if isinstance(text, str):  # Check if the synopsis is not a NaN (float)
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Tokenize text
        words = word_tokenize(text.lower())

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]

        return ' '.join(words)
    return ''

df['genres'] = df['genres'].apply(literal_eval)
df['genres'] = df['genres'].apply(lambda x: ' '.join(x))

df['synopsis'] = df['synopsis'].apply(preprocess_text)

# Create a TF-IDF Vectorizer to convert synopsis and genres into TF-IDF vectors
synopsis_vectorizer = TfidfVectorizer()
synopsis_tfidf = synopsis_vectorizer.fit_transform(df['synopsis'])

genre_vectorizer = TfidfVectorizer()
genre_tfidf = genre_vectorizer.fit_transform(df['genres'])

final_features = sp.hstack((genre_tfidf, synopsis_tfidf), format='csr')

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(final_features, final_features)

# Initialize the KNN model
knn_model = NearestNeighbors(n_neighbors=11, metric='cosine', algorithm='brute')  # Use 11 neighbors (including itself)

# Fit the model to the data (cosine similarity is already calculated, so we use fit() with the same data)
knn_model.fit(final_features)

# Save the fitted KNN model to a file
model_filename = 'knn_model.joblib'
joblib.dump((knn_model,final_features), model_filename)

print('Done')
