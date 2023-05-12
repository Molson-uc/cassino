import redis


r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

r.set("game_master:1", 0)
r.set("game_master:2", 0)
r.set("game_master:3", 0)

r.sadd("table:1", "game_master:1")
r.sadd("table:2", "game_master:2")
r.sadd("table:3", "game_master:3")

for i in range(1, 11):
    r.set(f"player:{i}", 10000)

for i in range(1, 4):
    r.sadd("table:1", f"player:{i}")

for i in range(4, 7):
    r.sadd("table:2", f"palyer:{i}")

for i in range(7, 10):
    r.sadd("table:3", f"player:{i}")
