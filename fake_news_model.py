import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class FakeNewsDetector:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

    def train(self, X_train, y_train):
        self.pipeline.fit(X_train, y_train)

    def predict(self, X):
        return self.pipeline.predict(X)

    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        return classification_report(y_test, y_pred)

def main():
    # Load the processed data
    train_df = pd.read_csv('data/processed_train.csv')
    test_df = pd.read_csv('data/processed_test.csv')

    # Initialize the model
    model = FakeNewsDetector()

    # Train the model
    model.train(train_df['statement'], train_df['label_encoded'])

    # Evaluate the model
    print(model.evaluate(test_df['statement'], test_df['label_encoded']))

if __name__ == "__main__":
    main()