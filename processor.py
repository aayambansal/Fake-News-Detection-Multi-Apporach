import threading
import queue
import time
from models.fake_news_model import FakeNewsDetector
from features.linguistic_features import AdvancedLinguisticFeatureExtractor
from credibility.source_credibility import SourceCredibilityAssessor

class RealTimeProcessor:
    def __init__(self):
        self.article_queue = queue.Queue()
        self.fake_news_detector = FakeNewsDetector()
        self.feature_extractor = AdvancedLinguisticFeatureExtractor()
        self.credibility_assessor = SourceCredibilityAssessor()
        self.processing_thread = threading.Thread(target=self._process_articles)
        self.is_running = False

    def start(self):
        self.is_running = True
        self.processing_thread.start()

    def stop(self):
        self.is_running = False
        self.processing_thread.join()

    def add_article(self, article_text, source_url):
        self.article_queue.put((article_text, source_url))

    def _process_articles(self):
        while self.is_running:
            try:
                article_text, source_url = self.article_queue.get(timeout=1)
                
                # Extract linguistic features
                linguistic_features = self.feature_extractor.extract_features(article_text)
                
                # Assess source credibility
                source_credibility = self.credibility_assessor.assess_credibility(source_url)
                
                # Detect fake news
                is_fake = self.fake_news_detector.predict([article_text])[0]
                
                # Combine results
                result = {
                    'is_fake': bool(is_fake),
                    'linguistic_features': linguistic_features,
                    'source_credibility': source_credibility
                }
                
                # Here you would typically send this result to a database or message queue
                print(f"Processed article from {source_url}: {result}")
                
            except queue.Empty:
                time.sleep(0.1)

    def get_queue_size(self):
        return self.article_queue.qsize()