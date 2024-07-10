from dhooks import Webhook, Embed
import time

class WebhookManager:
    def __init__(self, hookURL):
        self.hookURL = hookURL

    def cartCookie(self, cookieName, cookieValue, site, profile, sku, product, price, product_image, time, captcha):
        try:
            hook = Webhook(self.hookURL)
            embed = Embed(description='', color=1834808,timestamp='now',title='Complete Checkout!')

            embed.add_field(name='Site', value=site)
            embed.add_field(name='Profile', value=f'||{profile}||')
            embed.add_field(name='SKU', value=sku)
            embed.add_field(name='Product', value=product)
            embed.add_field(name='Price', value=price)
            embed.add_field(name='Checkout Speed', value=str(round(time, 2)) + ' s')
            embed.add_field(name='Captcha', value=str(captcha))
            embed.add_field(name=cookieName, value=f'||{cookieValue}||')
            embed.set_thumbnail(product_image)
        except:
            return

        while True:
            try:
                hook.send(embed=embed)
                return
            except:
                time.sleep(1)
                continue
