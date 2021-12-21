from flask import Flask, render_template, request, redirect, url_for
from recommender.recommender import Recommender
import random

app = Flask(__name__)


class AppState:
    def __init__(self):
        self.R = Recommender("data", emitter=self.set_emitter)
        self.search_results = []
        self.rec_results = []
        self.rec_mode = False
        self.add_like = self.R.add_like
        self.add_dislike = self.R.add_dislike
        self.remove = self.R.remove

        self.emissions = []

    def set_emitter(self, msg):
        self.emissions.append(msg)

    def add_neutral(self, s):
        old_emissions = self.emissions.copy()
        self.R.add_neutral(s)
        self.emissions = old_emissions

    @property
    def messages(self):
        return self.emissions[:-4:-1]

    def remove_rec(self, rec):
        old_emissions = self.emissions.copy()
        self.rec_results.remove(rec)
        self.emissions = old_emissions

    def recommend_like_likes(self):
        self.rec_results = self.R.recommend_like_likes()
        self.rec_mode = True

    def recommend_like_subset(self):
        try:
            names = ", ".join(random.sample(self.likes, k=3))
            self.emissions.append(f"Recommending based on {names}")
            old_emissions = self.emissions.copy()
            self.recommend_like_names(names)
            self.emissions = old_emissions
        except:
            self.emissions.append("Not enough likes to sample from (min 3).")

    def recommend_like_names(self, text):
        self.rec_results = self.R.recommend_like_names(text.split(","))
        self.rec_mode = True

    def search(self, text):
        self.search_results = self.R.search(text)
        self.rec_mode = False

    @property
    def likes(self):
        return list(self.R.liked)

    @property
    def dislikes(self):
        return list(self.R.disliked)

    @property
    def neutral(self):
        return list(self.R.neutral)


S = AppState()


@app.route('/')
def index():
    return render_template('index.html',
                           likes=S.likes,
                           dislikes=S.dislikes,
                           neutral=S.neutral,
                           search=S.search_results,
                           rec=S.rec_results,
                           rec_mode=S.rec_mode,
                           messages=S.messages)


@app.route('/recommend', methods=['POST'])
def recommend():
    text = request.form["rec"]
    if text:
        S.recommend_like_names(text)
    return redirect("/")


@app.route('/recommend-library', methods=['POST'])
def recommend_library():
    S.recommend_like_likes()
    return redirect("/")


@app.route('/recommend-subset', methods=['POST'])
def recommend_subset():
    S.recommend_like_subset()
    return redirect("/")


@app.route('/exclude', methods=['POST'])
def exclude():
    i = request.form["exclude"]
    S.add_neutral(i)
    S.remove_rec(i)
    return redirect("/")


@app.route('/add', methods=['POST'])
def add():
    try:
        i = request.form["addLike"]
        S.add_like(i)
    except KeyError:
        i = request.form["addDislike"]
        S.add_dislike(i)
    return redirect("/")


@app.route('/remove', methods=['POST'])
def remove():
    i = request.form["exclude"]
    S.remove(i)
    return redirect("/")


@app.route('/search', methods=['POST'])
def search():
    text = request.form["search"]

    if request.form["action"] == "Search":
        S.search(text)
    elif request.form["action"] == "Like":
        S.add_like(text)
    elif request.form["action"] == "Dislike":
        S.add_dislike(text)
    elif request.form["action"] == "Neutral":
        S.add_neutral(text)
    elif request.form["action"] == "Remove":
        S.remove(text)
    return redirect("/")


@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
