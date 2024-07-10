from cli import Logger
from webhooks import WebhookManager
import os, random, requests, json, time, threading

CARTED = 0
CHECKOUT = 0
FAILED = 0

lock = threading.Lock()

class BotBase:
    def __init__(self, site_name, task_id, settings):
        self.logger = Logger(site_name, task_id)
        self.webhook = WebhookManager(settings['Webhook'])
        self.settings = settings

    def getCaptchaToken(self, siteKey):
        while True:
            try:
                response = json.loads(requests.get('http://127.0.0.1:5000/api/token', data={'sitekey':siteKey}).text)
                if response['success']:
                    token = response['result']['token']
                    return token
                time.sleep(2)
            except Exception as e:
                time.sleep(2)
                continue

    def updateTaskData(self, key, data):
        lock.acquire()
        self.task_data[key] = data
        lock.release()

    def formatProxy(self):
        try:
            self.proxy = None
            if self.proxies == []:
                return None

            proxy = random.choice(self.proxies)
            proxy_parts = proxy.split(":")

            if len(proxy_parts) == 2:
                self.proxy = {"http": "http://" + proxy, "https": "https://" + proxy}
                return None

            elif len(proxy_parts) == 4:
                ip, port, user, passw = proxy_parts[0], proxy_parts[1], proxy_parts[2], proxy_parts[3]
                self.proxy = {
                    "http": "http://{}:{}@{}:{}".format(user, passw, ip, port),
                    "https": "http://{}:{}@{}:{}".format(user, passw, ip, port)
                }
                return None
        except:
            return None

    def updateStatusBar(self, value):
        global CARTED, CHECKOUT, FAILED

        if 'cart' in value:
            CARTED += 1
        elif 'checkout' in value:
            CHECKOUT += 1
        elif 'failed' in value:
            FAILED += 1

        os.system(f'title Checkouts: {str(CHECKOUT)} / Carted: {str(CARTED)} / Failed: {str(FAILED)}')
