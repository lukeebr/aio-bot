import threading, requests, time, random, json
from captcha.bank.server import startServer
from cli import Logger

class Harvester():
    def __init__(self, siteKey, url, siteName, version, captchaSolver, invisible='0', hostName='127.0.0.1', serverPort=5000):
        self.logger = Logger(siteName, 'RECAPTCHA HARVESTER')
        self.siteKey = siteKey
        self.url = url
        self.hostName = hostName
        self.serverPort = serverPort
        self.version = version
        self.invisible = invisible
        self.captchaSolver = captchaSolver

        if not self.serverRunning():
            threading.Thread(target=startServer).start()

        self.run()

    def serverRunning(self):
        try:
            serverStatus = requests.get('http://%s:%s' % (self.hostName, self.serverPort))

            if serverStatus.status_code == 200:
                return True
            else:
                return False
        except:
            return False

    def dumpToken(self, token):
        data = {
            'token':token,
            'sitekey':self.siteKey
        }

        sendToken = requests.post('http://%s:%s/api/submit' % (self.hostName, self.serverPort), data=data)
        response = json.loads(sendToken.text)

        if sendToken.status_code == 200 and response['success']:
            self.logger.success('Token saved')
        else:
            self.logger.error('Failed saving token')

    def getCaptchaToken(self):
        while True:
            try:
                self.logger.pending(f'Requesting ReCaptcha token from {self.captchaSolver.service}')
                token = self.captchaSolver.reCaptcha(self.siteKey, self.url, self.version, self.invisible)
                self.logger.info(f'Recieved ReCaptcha token from {self.captchaSolver.service} [{token[0:5]}...]')
                return token
            except:
                self.logger.error(f'Error requesting token from {self.captchaSolver.service}')
                time.sleep(5)
                continue

    def run(self):
        while True:
            token = self.getCaptchaToken()
            self.dumpToken(token)