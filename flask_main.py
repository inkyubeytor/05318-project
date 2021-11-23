from flask import Flask, render_template, request, redirect
from recommender.recommender import Recommender

app = Flask(__name__)

R = Recommender("data")


@app.route('/')
def index():
    return render_template('index.html',
                           likes=list(R.liked),
                           dislikes=list(R.disliked),
                           neutral=list(R.neutral),
                           search=R.search_results,
                           rec=R.rec_results,
                           rec_mode=R.rec_mode)


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form["search"]

    if request.form["action"] == "Recommend":
        if text:
            R.recommend_like_names(text.split(","))
        else:
            R.recommend_like_likes()
    elif request.form["action"] == "Search":
        R.search(text)
    elif request.form["action"] == "Like":
        R.add_like(text)
    elif request.form["action"] == "Dislike":
        R.add_dislike(text)
    elif request.form["action"] == "Neutral":
        R.add_neutral(text)
    elif request.form["action"] == "Remove":
        R.remove(text)
    return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)
