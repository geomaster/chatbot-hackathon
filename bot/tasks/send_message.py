from ..celery import celery_app as app
from pymessenger.bot import Bot
from secrets import ACCESS_TOKEN, APP_SECRET

bot = Bot(ACCESS_TOKEN, app_secret=APP_SECRET)

@app.task
def send_text_message(recipient_id, message):
    bot.send_text_message(recipient_id, message)

@app.task
def send_message(recipient_id, message):
    bot.send_message(recipient_id, message)

@app.task
def send_generic_message(recipient_id, elements):
    bot.send_generic_message(recipient_id, elements)

@app.task
def send_button_message(recipient_id, text, buttons):
    bot.send_button_message(recipient_id, text, buttons)

@app.task
def send_attachment(recipient_id, attachment_type, attachment_path):
    bot.send_attachment(recipient_id, attachment_type, attachment_path)

@app.task
def send_attachment_url(recipient_id, attachment_type, attachment_url):
    bot.send_attachment_url(recipient_id, attachment_type, attachment_url)

@app.task
def send_image(recipient_id, image_path):
    bot.send_image(recipient_id, image_path)

@app.task
def send_image_url(recipient_id, image_url):
    bot.send_image_url(recipient_id, image_url)

@app.task
def send_audio(recipient_id, audio_path):
    bot.send_audio(recipient_id, audio_path)

@app.task
def send_audio_url(recipient_id, audio_url):
    bot.send_audio_url(recipient_id, audio_url)

@app.task
def send_video(recipient_id, video_path):
    bot.send_video(recipient_id, video_path)

@app.task
def send_video_url(recipient_id, video_url):
    bot.send_video_url(recipient_id, video_url)

@app.task
def send_file(recipient_id, file_path):
    bot.send_file(recipient_id, file_path)

@app.task
def send_file_url(recipient_id, file_url):
    bot.send_file_url(recipient_id, file_url)

@app.task
def send_action(recipient_id, action):
    bot.send_action(recipient_id, action)

@app.task
def send_raw(payload):
    bot.send_raw(payload)
