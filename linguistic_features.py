import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from collections import Counter
import numpy as np
from textblob import TextBlob

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

class AdvancedLinguisticFeatureExtractor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def get_wordnet_pos(self, word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    def extract_features(self, text):
        # Tokenize the text
        sentences = sent_tokenize(text)
        tokens = word_tokenize(text.lower())
        
        # Remove stop words and lemmatize
        lemmas = [self.lemmatizer.lemmatize(token, self.get_wordnet_pos(token)) 
                  for token in tokens if token not in self.stop_words]
        
        # Calculate basic statistics
        num_tokens = len(tokens)
        num_unique_tokens = len(set(tokens))
        num_sentences = len(sentences)
        
        # Calculate lexical diversity
        lexical_diversity = num_unique_tokens / num_tokens if num_tokens > 0 else 0
        
        # Get most common lemmas
        most_common = Counter(lemmas).most_common(5)
        
        # Calculate average word and sentence length
        avg_word_length = np.mean([len(token) for token in tokens]) if tokens else 0
        avg_sentence_length = np.mean([len(word_tokenize(sent)) for sent in sentences]) if sentences else 0
        
        # Perform sentiment analysis
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Calculate readability (Flesch Reading Ease)
        if num_sentences > 0 and num_tokens > 0:
            words_per_sentence = num_tokens / num_sentences
            syllables_per_word = sum(self.count_syllables(word) for word in tokens) / num_tokens
            readability = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word
        else:
            readability = 0
        
        return {
            'num_tokens': num_tokens,
            'num_unique_tokens': num_unique_tokens,
            'num_sentences': num_sentences,
            'lexical_diversity': lexical_diversity,
            'most_common_lemmas': [word for word, _ in most_common],
            'avg_word_length': avg_word_length,
            'avg_sentence_length': avg_sentence_length,
            'sentiment': sentiment,
            'subjectivity': subjectivity,
            'readability': readability
        }

    def count_syllables(self, word):
        # This is a simple syllable counter and may not be 100% accurate
        vowels = 'aeiouy'
        count = 0
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count += 1
        return count