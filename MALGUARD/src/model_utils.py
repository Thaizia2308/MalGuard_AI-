# model_utils.py

import re
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import tldextract

# Regex to detect IP addresses in URLs
IP_RE = re.compile(r"^https?://\d+\.\d+\.\d+\.\d+")


class URLModelHelper:
    def __init__(self):
        # Character n-grams (2–5) on URL
        self.vec = TfidfVectorizer(analyzer='char', ngram_range=(2, 5), max_features=2000)

    def fit_transform_urls(self, urls):
        """Fit vectorizer and transform URLs into feature matrix."""
        tf = self.vec.fit_transform(urls)
        handcrafted = self._handcrafted_features(urls)
        X = np.hstack([tf.toarray(), handcrafted])
        return X

    def transform_urls(self, urls):
        """Transform new URLs using the trained vectorizer."""
        tf = self.vec.transform(urls)
        handcrafted = self._handcrafted_features(urls)
        X = np.hstack([tf.toarray(), handcrafted])
        return X

    def _handcrafted_features(self, urls):
        """Compute handcrafted features from URLs."""
        out = []
        suspicious_tlds = ['xyz', 'top', 'info']

        for u in urls:
            length = len(u)
            dots = u.count('.')
            has_ip = 1 if IP_RE.search(u) else 0
            has_at = 1 if '@' in u else 0
            uses_https = 1 if u.startswith('https') else 0

            # Extract TLD (top-level domain)
            ext = tldextract.extract(u)
            tld = ext.suffix.lower() if ext.suffix else ''
            suspicious = 1 if tld in suspicious_tlds else 0

            out.append([length, dots, has_ip, has_at, uses_https, suspicious])

        return np.array(out)

    def save(self, path):
        """Save model helper to disk."""
        joblib.dump(self, path)

    @staticmethod
    def load(path):
        """Load model helper from disk."""
        return joblib.load(path)
