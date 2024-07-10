from datetime import datetime
from termcolor import colored
from colorama import init
import threading

init()

lock = threading.Lock()

class Logger():
    def __init__(self, name, task_id):
        self.name = name
        self.task_id = task_id

    def success(self, message):
        lock.acquire()
        print(str(datetime.now().strftime("%H:%M:%S.%f")) + ' | ' + colored(self.name + ' ' * (11 - len(str(self.name))) + ' - ' + 'TASK ' + str(self.task_id) + ' ' * (4 - len(str(self.task_id))), 'yellow') + ' | ' + colored(message, 'green'))
        lock.release()

    def error(self, message):
        lock.acquire()
        print(str(datetime.now().strftime("%H:%M:%S.%f")) + ' | ' + colored(self.name + ' ' * (11 - len(str(self.name))) + ' - ' + 'TASK ' + str(self.task_id) + ' ' * (4 - len(str(self.task_id))), 'yellow') + ' | ' + colored(message, 'red'))
        lock.release()

    def pending(self, message):
        lock.acquire()
        print(str(datetime.now().strftime("%H:%M:%S.%f")) + ' | ' + colored(self.name + ' ' * (11 - len(str(self.name))) + ' - ' + 'TASK ' + str(self.task_id) + ' ' * (4 - len(str(self.task_id))), 'yellow') + ' | ' + colored(message, 'yellow'))
        lock.release()

    def info(self, message):
        lock.acquire()
        print(str(datetime.now().strftime("%H:%M:%S.%f")) + ' | ' + colored(self.name + ' ' * (11 - len(str(self.name))) + ' - ' + 'TASK ' + str(self.task_id) + ' ' * (4 - len(str(self.task_id))), 'yellow') + ' | ' + colored(message, 'white'))
        lock.release()