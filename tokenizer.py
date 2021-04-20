from collections import defaultdict
import argparse

def tokenize(text):
    tokens = list()
    valid = True
    alphanumeric = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'"
    for word in text.split(" "):
        valid = True
        for char in word:
            if char not in alphanumeric:
                valid = False
        if len(word) > 1 and valid == True:
            tokens.append(word.lower())
    return tokens

def compute_word_frequencies(tokens: list):
    mapped_tokens = defaultdict(int)
    for token in tokens:
        mapped_tokens[token] += 1
    return dict(mapped_tokens)
