from redis import StrictRedis

redis = StrictRedis(unix_socket_path="/var/run/redis/redis.sock")
