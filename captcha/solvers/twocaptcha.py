import requests, time

class TwoCaptcha():
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.service = '2Captcha'
        self.session = requests.session()
        self.session.params = {'key':self.apiKey}

    def reCaptcha(self, siteKey, url, version='v2', invisible='0'):
        params = {
            'googlekey':siteKey,
            'pageurl':url,
            'method':'userrecaptcha',
            'invisible':invisible,
            'version':version
        }
        
        response = self.session.post('http://2captcha.com/in.php', params=params)

        captchaID = response.text.split('|')[1]

        payload = {
            'id':captchaID,
            'action':'get'
        }

        while True:
            response = self.session.get('http://2captcha.com/res.php', params=payload)

            if 'CAPCHA_NOT_READY' in response.text:
                time.sleep(5)
                continue

            if not response.text.startswith('OK|'):
                raise Exception

            return response.text[3:]
