# src/dictionary.py
import csv
import os

class Dictionary:
    def __init__(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset not found: {filepath}")

        self.word_freq = {}
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)  # expects header: word,count
            for row in reader:
                word = row["word"].strip().lower()
                freq = int(row["count"])   # ✅ use 'count'
                self.word_freq[word] = freq

    def get_words(self):
        return list(self.word_freq.keys())

    def get_freq(self, word):
        return self.word_freq.get(word.lower(), 0)
