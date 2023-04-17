from .models import *
import threading
from views import *


class CreateThread(threading.Thread):
    def __init__(self, command):
        self.command = command
        threading.Thread.__init__(self)

    def run(self):
        try:
            print("thread started")

        except Exception as e:
            print(e)
