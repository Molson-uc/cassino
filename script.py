import redis
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")


def set_dataset():
    r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

    r.set("game_master:1:stack", 0)
    r.set("game_master:2:stack", 0)
    r.set("game_master:3:stack", 0)

    r.sadd("table:1", "game_master:1")
    r.sadd("table:2", "game_master:2")
    r.sadd("table:3", "game_master:3")

    for i in range(1, 11):
        r.set(f"player:{i}:stack", 10000)
        r.set(f"player:{i}:name", f"Name{i}")

    for i in range(1, 4):
        r.sadd("table:1", f"player:{i}:stack")

    for i in range(4, 7):
        r.sadd("table:2", f"palyer:{i}:stack")

    for i in range(7, 10):
        r.sadd("table:3", f"player:{i}:stack")


if __name__ == "__main__":
    set_dataset()
