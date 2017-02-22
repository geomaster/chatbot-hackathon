class MockUserState:
    def __init__(self):
        self.state_id = None
        self.attrs = {}

    def get_key(self, key):
        return self.attrs.get(key)

    def set_key(self, key, value):
        self.attrs["key"] = value

    def get_state_id(self):
        return self.state_id

    def set_state_id(self, state_id):
        self.state_id = state_id

class RedisUserState:
    def __init__(self, user_id, redis):
        self.object_id = "user:{0}".format(user_id)
        self.redis = redis

    def get_key(self, key):
        return self.redis.hget(self.object_id, key).decode("utf-8")

    def set_key(self, key, value):
        return self.redis.hset(self.object_id, key, value)

    def get_state_id(self):
        return self.redis.hget(self.object_id, "state_id").decode("utf-8")

    def set_state_id(self, state_id):
        self.redis.hset(self.object_id, "state_id", state_id)
