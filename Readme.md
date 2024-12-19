# README: Loading and Using a Trained Model in Jupyter Notebook

This README will guide you through the steps to load and use a pre-trained model file with a `.pkl` or `.h5` for the RNN with LSTM layer model

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.x
- Jupyter Notebook
- Required libraries:
    - `pickle` (for loading the `.pkl` model)
    - `scikit-learn` or any other library relevant to your model (e.g., `tensorflow`, `keras` for deep learning models)

You can install the necessary libraries using `pip`:

```bash
pip install scikit-learn
```

## Import a pre-trained model
To import a pre-trained model, execute this python script

```python
from tensorflow.keras.models import load_model

# Load the model from the file
model = load_model('LSTM.h5')
model = load_model('random_forest.pkl')
```

To predict a sentence using the model you can execute this python script:
```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # Adjust max_features based on dataset size

example_sentence = ["أحيانًا تزداد الغيرة عندما نرى الآخرين يحققون ما نرغب في الوصول إليه"]
example_tfidf = tfidf_vectorizer.transform(example_sentence)
predicted_category = random_forest_model.predict(example_tfidf)
print(f"Predicted Category: {predicted_category[0]}")
```



