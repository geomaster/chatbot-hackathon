import json
import time
import sys
from flask import Flask, request, redirect, render_template, send_from_directory
from server.secrets import EXPECTED_VERIFY_TOKEN
from bot.tasks.handle_message import handle_message

app = Flask("pcr-test-bot")

@app.route("/")
def index():
    return "Welcome to <code>pcr-test-bot</code> backend."

@app.route("/webhook", methods=["GET"])
def webhook_verify():
    args = request.args
    if "hub.challenge" in args.keys():
        if args.get("hub.verify_token") != EXPECTED_VERIFY_TOKEN:
            return "Invalid verification token.", 403
        else:
            return request.args["hub.challenge"], 200
    else:
        return redirect("/", 301)

@app.route("/webhook", methods=["POST"])
def webhook_post():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for event in entry["messaging"]:
                if "message" in event.keys():
                    sender = event["sender"]["id"]
                    msg = event["message"]
                    timestamp = event["timestamp"]
                    handle_message.delay(sender, msg, timestamp)

    return "ok", 200

@app.route('/dashboard/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/dashboard")
def dashboard_index():
    return redirect("/dashboard/questions", 301)

@app.route("/dashboard/questions")
def dashboard_questions():
    return render_template("questions.html")

@app.route("/dashboard/surveys")
def dashboard_surveys():
    return render_template("surveys.html")


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="127.0.0.1", port=9889)
