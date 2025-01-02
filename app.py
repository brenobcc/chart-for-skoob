from flask import Flask, render_template, request
from helpers.processor import startProcess

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        user_id = request.form["user_id"]
        column = int(request.form["column"])
        line = int(request.form["line"])

        paste_star = "paste_star" in request.form

        return startProcess(user_id, column, line, paste_star)

    return render_template("homepage.html")

if __name__ == "__main__":
    app.run(debug=True)