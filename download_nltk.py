import nltk
import ssl
# Fix for some deployment environments
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print("Checking and downloading NLTK data...")

nltk.download('stopwords')
nltk.download('punkt')

print("NLTK data download complete.")