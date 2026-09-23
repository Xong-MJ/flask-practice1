from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", name="송민준", student_id="24013813")

@app.route("/profile")
def profile():
    hobbies = ["춤추기", "노래부르기", "게임하기"]
    return render_template("profile.html", hobbies=hobbies)

if __name__ == "__main__":
    app.run(debug=True)
