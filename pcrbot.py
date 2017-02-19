from flask import Flask
app = Flask("pcr-test-bot")

@app.route("/")
def index():
    return "Welcome to <code>pcr-test-bot</code> backend."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9889)
