from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", name="송민준", student_id="24013813")

if __name__ == "__main__":
    app.run(debug=True)
