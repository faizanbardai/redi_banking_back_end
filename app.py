from flask import Flask

app = Flask(__name__)

@app.route("/")
def banking_app():
    return "<p>Banking App!</p>"