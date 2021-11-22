"""
Create document vectors for each chapter.
"""
import spacy
import os
import numpy as np


class Vectorizer:
    def __init__(self, path):
        self.path = path
        self.nlp = spacy.load("en_core_web_lg")

    def vectorize_fic(self, path):
        out = np.zeros((10, 300))
        files = set(os.listdir(path))
        for i in range(1, 11):
            fname = f"{i}.txt"
            if fname in files:
                with open(f"{path}/{fname}", "r", encoding="utf-8") as f:
                    text = f.read()
                doc = self.nlp(text)
                out[i - 1] = doc.vector
        np.save(f"{path}/vecs.npy", out)

    def vectorize(self):
        data_dirs = os.listdir(f"{self.path}/fics")
        for data_dir in data_dirs:
            path = f"{self.path}/fics/{data_dir}"
            if "vecs.npy" not in os.listdir(path):
                print(f"Vectorizing {data_dir}")
                self.vectorize_fic(path)
            else:
                print(f"Skipping {data_dir}")


if __name__ == "__main__":
    vectorizer = Vectorizer("../data")
    vectorizer.vectorize()
