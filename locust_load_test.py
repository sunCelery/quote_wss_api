# "http://localhost:8000"
import time
import json
from locust import task
from locust_plugins.users import SocketIOUser


class MySocketIOUser(SocketIOUser):
    max_wait = 1
    min_wait = 1
    user_count = 1500
    spawn_rate = 250

    def on_start(self):
        self.connect("ws://localhost:8000/courses")

    @task(1)
    def my_task1(self):
        self.my_value = None

        # self.connect("ws://localhost:8000/courses")

        # example of subscribe
        self.send('42["subscribe",{"url":"/courses","sendInitialUpdate": true}]')

        # wait until I get a push message to on_message
        # while not self.my_value:
        #     time.sleep(0.01)

        # wait for additional pushes, while occasionally sending heartbeats, like a real client would
        self.sleep_with_heartbeat(1)

    @task(1)
    def my_task2(self):
        self.my_value = None

        # self.connect("ws://localhost:8000/BTC-USDT")

        # example of subscribe
        self.send('42["subscribe",{"url":"/BTC-USDT","sendInitialUpdate": true}]')

        # wait until I get a push message to on_message
        # while not self.my_value:
        #     time.sleep(0.01)

        # wait for additional pushes, while occasionally sending heartbeats, like a real client would
        self.sleep_with_heartbeat(1)

    def on_message(self, message):
        self.my_value = json.loads(message)["BTC-USDT"]


if __name__ == "__main__":
    host = "http://localhost:8000"
    MySocketIOUser.protocol = "ws"
