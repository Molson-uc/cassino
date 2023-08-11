from django_redis import get_redis_connection
import redis
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")


class Transaction:
    def __init__(self) -> None:
        self.db = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
        self.lau_transaction = """
        if KEYS[1]~=KEYS[2] then
            redis.call('DECRBY', KEYS[1], ARGV[1])
            redis.call('INCRBY', KEYS[2], ARGV[1])
        end
        """

        self.lau_recharge = """
        redis.call('INCRBY', KEYS[1], ARGV[1])
        """

        self.transaction = self.db.script_load(self.lau_transaction)
        self.recharge = self.db.script_load(self.lau_recharge)

    def transaction_execute(self, source, target, money):
        pipe = self.db.pipeline(transaction=True)
        pipe.evalsha(self.transaction, 2, source, target, money)
        pipe.execute()

    def recharge_execute(self, target, money):
        pipe = self.db.pipeline(transaction=True)
        pipe.evalsha(self.recharge, 1, target, money)
        pipe.execute()


def test_redis():
    redis_conn = get_redis_connection("default")
    print(redis_conn)
