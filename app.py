from flask import Flask, render_template
from external_api import external_api_bp
from api import coins_bp

app = Flask(__name__)

app.register_blueprint(external_api_bp)
app.register_blueprint(coins_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
