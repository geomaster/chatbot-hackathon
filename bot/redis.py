from redis import Redis

redis = Redis(unix_socket_path="/var/run/redis/redis.sock")
