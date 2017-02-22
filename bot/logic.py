def handle(user_state, meaning, send_fn):
    s = user_state.get_state_id()
    send_fn({
        "text": "Hello world from state_transition! You are in state" \
            " {0}".format(s),
        "quick_replies": [{
            "content_type": "text",
            "title": "yo",
            "payload": "empty"
        }, {
            "content_type": "text",
            "title": "oyy",
            "payload": "empty"
        }, {
            "content_type": "text",
            "title": "xD",
            "payload": "empty"
        }]
    })

    return s == "testStateTrue" and "testStateFalse" or "testStateTrue"
