from .doc_vector import Vectorizer
import os
import numpy as np
from thefuzz import process


class Indexer:
    def __init__(self, path):
        self.path = path
        self.index_path = f"{self.path}/fics_index.txt"

    def make_index(self):
        fics = os.listdir(f"{self.path}/fics")
        with open(self.index_path, "w+") as f:
            f.write("\n".join(f"{i}\t{name}" for i, name in enumerate(fics)))

    def load_index(self):
        with open(self.index_path, "r") as f:
            lines = f.readlines()
        index = []
        for line in lines:
            i, name = line.strip().split("\t")
            assert len(index) == int(i)
            index.append(name)
        return index

    def make_avg_array(self):
        index = self.load_index()
        vecs = np.zeros((len(index), 300))
        for i, fic in enumerate(index):
            vecs[i] = Vectorizer.read_avg_vector(f"{self.path}/fics/{fic}")

        np.save(f"{self.path}/index_vecs.npy", vecs)


class User:
    def __init__(self):
        self.liked = set()
        self.disliked = set()
        self.neutral = set()

    @property
    def read(self):
        return self.liked | self.disliked | self.neutral


class Recommender:
    def __init__(self, path):
        self.path = path

        indexer = Indexer(self.path)
        self.index = indexer.load_index()
        self.legible_index = self.parse_index()

        A = np.load(f"{self.path}/index_vecs.npy")
        self.index_vecs = (A.T / np.linalg.norm(A, axis=1)).T

        self.user = User()

        self.search_results = []
        self.rec_results = []
        self.rec_mode = False

    def parse_index(self):
        return [entry.replace("-", " ") for entry in self.index]

    def search(self, string, k=5):
        results = process.extractBests(string,
                                       self.legible_index,
                                       score_cutoff=90,
                                       limit=k)
        results = [x for x, _ in sorted(results,
                                        key=lambda y: y[1],
                                        reverse=True)]
        self.search_results = results
        self.rec_mode = False
        return results

    def match_best(self, string):
        match = process.extractOne(string, self.legible_index)[0]
        if string != match:
            print(f"Assuming you meant {match}")
        return self.legible_index.index(match)

    def recommend_like_indices(self, indices, recs=5):
        exclude = self.user.read | set(indices)
        composite_vec = sum(self.index_vecs[i] for i in indices)
        composite_vec /= np.linalg.norm(composite_vec)
        scores = self.index_vecs @ composite_vec
        scored_indices = [(i, score) for i, score in enumerate(scores)
                          if i not in exclude]
        scored_indices.sort(key=lambda x: x[1], reverse=True)
        recs = [self.legible_index[i] for i, _ in scored_indices[:recs]]
        self.rec_results = recs
        self.rec_mode = True
        return recs

    def recommend_like_names(self, names, recs=5):
        matches = [self.match_best(s) for s in names]
        return self.recommend_like_indices(matches, recs)

    def recommend_like_likes(self):
        return self.recommend_like_indices(list(self.user.liked))

    def add_like(self, s):
        i = self.match_best(s)
        self.user.liked.add(i)
        self.user.disliked.discard(i)
        self.user.neutral.discard(i)

    def add_dislike(self, s):
        i = self.match_best(s)
        self.user.liked.discard(i)
        self.user.disliked.add(i)
        self.user.neutral.discard(i)

    def add_neutral(self, s):
        i = self.match_best(s)
        self.user.liked.discard(i)
        self.user.disliked.discard(i)
        self.user.neutral.add(i)

    def remove(self, s):
        i = self.match_best(s)
        self.user.liked.discard(i)
        self.user.disliked.discard(i)
        self.user.neutral.discard(i)

    @property
    def liked(self):
        return [self.legible_index[i] for i in self.user.liked]

    @property
    def disliked(self):
        return [self.legible_index[i] for i in self.user.disliked]

    @property
    def neutral(self):
        return [self.legible_index[i] for i in self.user.neutral]



if __name__ == "__main__":
    indexer = Indexer("../data")
    indexer.make_index()
    indexer.make_avg_array()
    R = Recommender("../data")
