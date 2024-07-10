from base import BotBase
from bs4 import BeautifulSoup
import cloudscraper, helheim, time, json, random

from helheim.exceptions import (
    HelheimException,
    HelheimSolveError,
    HelheimRuntimeError,
    HelheimSaaSError,
    HelheimSaaSBalance,
    HelheimVersion,
    HelheimAuthError
)

helheim.auth('4504e04b-59f3-4a6a-a3d0-262a7536ff5c')



class Stress95(BotBase):
    def __init__(self, task, proxies, task_id, settings, task_data):
        BotBase.__init__(self, 'Stress95', task_id, settings)
        self.task_id = task_id
        self.task = task
        self.proxies = proxies
        self.delay = float(self.task['Delay'])
        self.link = self.task['Link']
        self.size = self.task['Size']
        self.task_data = task_data
        self.settings = settings
        self.formatProxy()

        self.session = cloudscraper.create_scraper(browser={'browser': 'chrome','mobile': False,'platform': 'windows'},requestPostHook=self.injection,captcha={'provider': 'vanaheim'})
        
        if self.proxy:
            self.session.proxies = self.proxy

        helheim.wokou(self.session)
        
        self.monitor()
        self.atc()

    def injection(self, session, response):
        if helheim.isChallenge(session, response):
            self.logger.pending('Solving Cloudflare...')
            return helheim.solve(session, response)
        else:
            return response

    def monitor(self):

        self.startTime = time.time()

        while True:
            instock = []
            
            self.logger.pending('Getting product page')

            try:
                response = self.session.get(self.link)
            except Exception as e:
                self.logger.error(f'Exception getting product: {e}')
                time.sleep(self.delay)
                continue

            if response.status_code != 200:
                self.logger.error(f'Error getting product [{response.status_code}]')
                time.sleep(self.delay)
                continue
            else:

                try:
                    stocksoup = BeautifulSoup(response.text, 'html.parser')
                except:
                    self.logger.error('Exception loading page')
                    time.sleep(self.delay)
                    continue

                try:
                    productData = json.loads(stocksoup.find('script', {'id':'product-form-data'}).text)
                except:
                    self.logger.error('Exception loading product data')
                    time.sleep(self.delay)
                    continue

                try:
                    self.captchaActive = productData['reCaptchaActive']
                except:
                    self.logger.error('Error loading ReCaptcha status')
                    time.sleep(self.delay)
                    continue
                
                try:
                    productJSON = productData['products']
                except:
                    self.logger.error('Error loading stock')
                    time.sleep(self.delay)
                    continue
                
                try:
                    for product in productJSON:
                        if productJSON[product]['unitsAvailable'] != 0:
                            instock.append({'size':productJSON[product]['EU']['Value'], 'sku':productJSON[product]['id']})
                except:
                    self.logger.error('Error parsing sizes')
                    time.sleep(self.delay)
                    continue

                if len(instock) == 0:
                    self.logger.error('Product OOS')
                    time.sleep(self.delay)
                    continue

                if self.size.lower().strip() == 'random' or self.size.lower().strip() == 'any':
                    self.size = random.choice(instock)
                    self.sku = self.size['sku']
                    self.logger.success(f'Found random size: {self.size["size"]}')
                    stocksoup.decompose()
                    return
                else:
                    for item in instock:
                        if item['size'] == self.size.strip():
                            self.logger.success(f'Found size: {item["size"]}')
                            self.sku = item['sku']
                            self.size = item['size']
                            return

                    self.logger.error('Desired size not found')
                    time.sleep(self.delay)
                    continue

    def atc(self):
        while True:

            self.logger.pending('Adding product to cart')

            data = {
                'id':self.sku,
                'partial':'ajax-cart'
            }

            if self.captchaActive:
                self.logger.pending('Getting captcha token')
                captchaToken = self.getCaptchaToken('6LfSdnwUAAAAAF6vZ9LbeVbMCZNcTiw3VGdBK_Y9')
                data['g-recaptcha-response'] = captchaToken

            try:
                atc = self.session.post('https://stress95.com/cart/add', data=data)
            except Exception as e:
                self.logger.error(f'Exception adding product to cart: {e}')
                time.sleep(self.delay)
                continue

            if atc.status_code != 200:
                self.logger.error(f'Failed adding product to cart [{atc.status_code}]')
                time.sleep(self.delay)
                continue
            else:
                try:
                    cartsoup = BeautifulSoup(atc.text, 'html.parser')
                except:
                    pass

                try:
                    self.prodName = cartsoup.find('span', {'class':'cart-item-display-name'}).text.strip()
                except:
                    self.prodName = '?'

                try:
                    self.prodPrice = cartsoup.find('span', {'class':'sub-total'}).text.strip()
                except:
                    self.prodPrice = '?'

                try:
                    self.prodImage = 'https://stress95.com' + cartsoup.find('div', {'class':'cart-item-img'}).findChildren('img')[0]['src']
                except:
                    self.prodImage = None

                self.logger.success(f'Successfully added {self.prodName} to cart')
                self.elapsedTime = (time.time() - self.startTime)
                self.cartCookie = self.session.cookies['png.state']
                self.logger.info(f'PNG.STATE > {self.cartCookie}')
                self.webhook.cartCookie('png.state', self.cartCookie, 'Stress95', self.task['Profile Name'], self.sku, self.prodName, self.prodPrice, self.prodImage, self.elapsedTime, self.captchaActive)
                self.updateStatusBar('cart')
                return           

