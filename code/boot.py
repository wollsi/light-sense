import ujson

with open("config.json") as f:
        __data = ujson.load(f)

sleep_time = __data["sleep_time"]