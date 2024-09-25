import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

class SourceCredibilityAssessor:
    def __init__(self):
        self.trusted_domains = set(['bbc.com', 'nytimes.com', 'reuters.com', 'apnews.com'])
        self.blacklisted_domains = set(['fakenews.com', 'conspiracytheories.net'])

    def assess_credibility(self, url):
        domain = urlparse(url).netloc
        
        if domain in self.trusted_domains:
            return 1.0
        elif domain in self.blacklisted_domains:
            return 0.0
        
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for presence of author information
            author_present = bool(soup.find('meta', attrs={'name': 'author'}))
            
            # Check for presence of publication date
            date_present = bool(soup.find('meta', attrs={'name': 'publication_date'}))
            
            # Check for presence of sources or references
            text = soup.get_text()
            sources_present = bool(re.search(r'source|reference|according to', text, re.IGNORECASE))
            
            # Check for HTTPS
            https_present = url.startswith('https')
            
            # Calculate credibility score
            score = (author_present + date_present + sources_present + https_present) / 4
            
            return score
        
        except:
            return 0.5  # Return neutral score if unable to assess

    def get_domain_reputation(self, domain):
        # This would typically involve querying a reputation database or API
        # For this example, we'll return a random score
        import random
        return random.uniform(0, 1)