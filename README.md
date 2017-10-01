# Chatbot Hackathon Project

**The code in this repository has been created for a hackathon, and so it
contains unfinished work and is generally unpolished.**

Code for a Facebook Messenger chatbot that can provide answers to Telenor Serbia
related questions by searching its forums and querying its databases. It also
asks users to answer surveys (with prior consent), the results of which can be
visualized and analyzed using a simple dashboard.

The chatbot uses Telenor's data sources, as well as Api.ai for natural language
processing. The back end is a Flask web server backed by a Redis data store and
asynchronous task management based on Celery. The dashboard is a web application
that uses the Semantic UI framework and the C3 JavaScript framework (for charts).

![Dashboard Screenshot](/screenshots/dashboard.png?raw=true "Dashboard Screenshot")

The repository also contains an unfinished editor for a tree-based conversational
model, alongside its (also unfinished) implementation. The editor generates a
conversational tree in a JSON-based format, allowing easy incorporation into a
chatbot.

![Editor Screenshot](/screenshots/editor.png?raw=true "Editor Screenshot")
