from flask import Flask, request, redirect
from server.secrets import EXPECTED_VERIFY_TOKEN
import json
import time
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
                    print("[{0}] Dispatched task at {1}".format(msg["mid"], time.time()))
                    handle_message.delay(sender, msg)

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9889)
