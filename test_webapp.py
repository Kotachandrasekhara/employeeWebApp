from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # name = request.args.get("name", "World")
    return "Hello World"

