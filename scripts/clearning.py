import os
import pandas as pd
import re
import nltk
from camel_tools.tokenizers.word import simple_word_tokenize
from nltk.corpus import stopwords
from nltk.stem.isri import ISRIStemmer
from tqdm import tqdm

# Download NLTK stopwords for Arabic (if not already downloaded)
nltk.download('stopwords')

# Load Arabic stopwords
arabic_stopwords = set(stopwords.words('arabic'))

# Initialize the ISRIStemmer for stemming Arabic words
stemmer = ISRIStemmer()

# Function to normalize Arabic text (remove diacritics, normalize letters)


def normalize_arabic(text):
    # Remove diacritics (vowel marks)
    # Unicode range for Arabic diacritics
    diacritic_pattern = re.compile(r'[\u064B-\u0652]')
    text = diacritic_pattern.sub('', text)
    # Normalize some common Arabic characters (this can be extended)
    text = text.replace("ى", "ي").replace("ئ", "ي").replace("ؤ", "و")
    return text

# Function to remove stopwords


def remove_stopwords(text):
    tokens = simple_word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in arabic_stopwords]
    return ' '.join(filtered_tokens)

# Function to tokenize Arabic text


def tokenize_text(text):
    return simple_word_tokenize(text)

# Function to remove non-Arabic characters


def remove_non_arabic(text):
    return re.sub(r'[^ء-ي\s]', '', text)

# Optional: Function for standardization (example: specific word replacements)


def standardize_arabic(text):
    # Example: Standardizing certain common words
    text = text.replace("الله", "اللّه")
    return text

# Function to apply stemming to Arabic text


def stem_arabic(text):
    tokens = simple_word_tokenize(text)
    stemmed_tokens = [stemmer.stem(word) if len(
        word) > 3 else word for word in tokens]
    return ' '.join(stemmed_tokens)

# Complete preprocessing pipeline


def preprocess_text(text):
    text = normalize_arabic(text)  # Normalize the text
    text = remove_non_arabic(text)  # Remove non-Arabic characters
    text = remove_stopwords(text)  # Remove stopwords
    text = stem_arabic(text)  # Apply stemming
    text = standardize_arabic(text)  # Optional: Apply standardization
    tokens = tokenize_text(text)   # Tokenize the text
    return tokens


# Load the CSV data
FOLDER_NAME = 'Data/'
input_file = "test.csv"
input_file_path = os.path.join(FOLDER_NAME, input_file)
output_file = "merged_dhia.csv"
output_file_path = os.path.join(FOLDER_NAME, output_file)
df = pd.read_csv(input_file_path, sep=',', encoding='utf-8')

# Apply preprocessing to the 'quote' column (adjust column name as necessary)
processed_quotes = []

# Loop through each row and apply preprocessing with tqdm progress bar
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows"):
    text = row['Line']

    # Apply the preprocessing to each line of text
    processed_tokens = preprocess_text(text)

    # Filter out lines with empty tokens or tokens composed only of '-'
    if len(processed_tokens) == 0 or all(token == '-' for token in processed_tokens):
        processed_tokens = []

    # Append the processed tokens to the list
    processed_quotes.append(processed_tokens)

# Now add the processed quotes back to the DataFrame as a new column
# Adjust DataFrame size to match the filtered tokens
df = df.iloc[:len(processed_quotes)]
df['processed_quotes'] = processed_quotes
df_filtered = df[df['processed_quotes'].apply(lambda x: len(x) > 0)]
# Preview the cleaned data
print(df[['Line', 'processed_quotes']].head())

# Save the cleaned data to a new CSV file
df_filtered.to_csv(output_file_path, index=False)
