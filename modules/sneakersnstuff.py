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

class SNS(BotBase):
    def __init__(self, task, proxies, task_id, settings, task_data):
        BotBase.__init__(self, 'SNS', task_id, settings)
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
                    soup = BeautifulSoup(response.text, 'html.parser')
                    self.soup = BeautifulSoup(response.text, 'html.parser')
                except:
                    self.logger.error('Exception loading page')
                    time.sleep(self.delay)
                    continue

                try:
                    self.did = soup.find('input', {'name':'did'})['value']
                except:
                    self.logger.error('Exception fetching did value')
                    time.sleep(self.delay)
                    continue

                try:
                    self.csrfToken = soup.find('input', {'name':'_AntiCsrfToken'})['value']
                except:
                    self.logger.error('Error fetching CSRF token')
                    time.sleep(self.delay)
                    continue

                try:
                    self.prodName = soup.find('meta', {'property':'og:title'})['content']
                except:
                    self.prodName = '?'

                try:
                    self.prodPrice = soup.find('span', {'class':'price'})['data-value']
                except:
                    self.prodPrice = '?'
                
                try:
                    self.prodImage = soup.findAll('meta', {'property':'og:image'})[0]['content']
                except:
                    self.prodImage = '?'

                try:
                    self.captchaActive = True if (soup.find('div', {'class':'g-recaptcha'})) is not None else False
                except:
                    self.logger.error('Error loading ReCaptcha status')
                    time.sleep(self.delay)
                    continue
                
                try:
                    sizes = soup.find('ul', {'class':'product-sizes'}).findChildren()
                except:
                    self.logger.error('Error loading sizes')
                    time.sleep(self.delay)
                    continue

                try:
                    for size in sizes:
                        size_elements = size.findChildren()
                        
                        if len(size_elements) != 3:
                            continue

                        if size_elements[0].has_attr('disabled'):
                            continue

                        sku = size_elements[0]['value']
                        size = size_elements[2].text

                        instock.append({'size':size, 'sku':sku})
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
                    soup.decompose()
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
                'did':self.did,
                'id':self.sku,
                'partial':'mini-cart'
            }

            for x in self.soup.findAll('img'):
                try:
                    print(self.session.get('https://www.sneakersnstuff.com' + x['src']).status_code)
                except:
                    pass
                
            if self.captchaActive:
                self.logger.pending('Getting captcha token')
                captchaToken = self.getCaptchaToken('6LeKIW0UAAAAAA-ouoKHOnWuQDNymSwDFYeGP323')
                data['g-recaptcha-response'] = captchaToken
                
            try:
                atc = self.session.post('https://www.sneakersnstuff.com/en/cart/add', json=data)
            except Exception as e:
                self.logger.error(f'Exception adding product to cart: {e}')
                time.sleep(self.delay)
                continue

            print(atc.text)

            if atc.status_code != 200:
                self.logger.error(f'Failed adding product to cart [{atc.status_code}]')
                time.sleep(self.delay)
                continue
            else:
                self.logger.success(f'Successfully added {self.prodName} to cart')
                self.elapsedTime = (time.time() - self.startTime)
                self.cartCookie = self.session.cookies['png.state']
                self.logger.info(f'PNG.STATE > {self.cartCookie}')
                self.webhook.cartCookie('png.state', self.cartCookie, 'SNS', self.task['Profile Name'], self.sku, self.prodName, self.prodPrice, self.prodImage, self.elapsedTime, self.captchaActive)
                self.updateStatusBar('cart')
                return           

