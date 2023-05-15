from django_redis import get_redis_connection

import redis
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")


def test_redis():
    redis_conn = get_redis_connection("default")
    print(redis_conn)


class Transation:
    def __init__(self) -> None:
        self.db = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
        self.lau_transfer = """
        redis.call('DECRBY', KEYS[1], ARGV[1])
        redis.call('INCRBY', KEYS[2], ARGV[1])
        """
        self.transfer = self.db.script_load(self.lau_transfer)
        print(self.transfer)

    def transaction(self, source, target, money):
        pipe = self.db.pipeline(transaction=True)

        pipe.evalsha(self.transfer, 2, source, target, money)
        print(self.transfer)
        pipe.execute()
