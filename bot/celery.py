from celery import Celery

task_routes = {
    'bot.tasks.handle_message.handle_message': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_action': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_attachment': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_attachment_url': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_audio': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_audio_url': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_button_message': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_file': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_file_url': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_generic_message': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_image': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_image_url': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_message': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_raw': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_text_message': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_video': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_message.send_video_url': {'queue': 'celery', 'delivery_mode': 'transient'},
    'bot.tasks.send_text_message': {'queue': 'celery', 'delivery_mode': 'transient'}
}

celery_app = Celery("bot",
                    broker="redis+socket:///var/run/redis/redis.sock",
                    include=["bot.tasks"],
                    task_routes=task_routes)

if __name__ == "__main__":
    celery_app.start()
