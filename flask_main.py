from flask import Flask, render_template, request, redirect, flash
from recommender.recommender import Recommender

app = Flask(__name__)


class AppState:
    def __init__(self):
        self.R = Recommender("data", emitter=self.set_emitter)
        self.search_results = []
        self.rec_results = []
        self.rec_mode = False
        self.add_like = self.R.add_like
        self.add_dislike = self.R.add_dislike
        self.add_neutral = self.R.add_neutral
        self.remove = self.R.remove

        self.emission = None

    def set_emitter(self, msg):
        self.emission = msg

    def recommend_like_likes(self):
        self.rec_results = self.R.recommend_like_likes()
        self.rec_mode = True

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
                           rec_mode=S.rec_mode)


@app.route('/recommend', methods=['POST'])
def recommend():
    text = request.form["rec"]
    if text:
        S.recommend_like_names(text)
    else:
        S.recommend_like_likes()
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


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)

