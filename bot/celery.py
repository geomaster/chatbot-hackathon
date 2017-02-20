from celery import Celery

celery_app = Celery("bot",
                    broker="amqp://localhost",
                    backend="amqp://localhost",
                    include=["bot.tasks"])

if __name__ == "__main__":
    celery_app.start()
