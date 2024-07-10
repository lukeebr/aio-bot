import time, csv, codecs, glob, inquirer, sys, os, json, threading, datetime
from pyfiglet import Figlet
from utils import UITheme
from termcolor import colored
from inquirer import themes
from tasks import TaskManager
from captcha.bank.harvester import Harvester
from captcha.solvers.twocaptcha import TwoCaptcha

VERSION = '0.0.1'

class Main:
    def __init__(self):
        self.cls = lambda : os.system('cls')

        self.loadSettings()
        self.menu()

    def menu(self):
        self.cls()

        f = Figlet(font="slant", justify="center")
        print("\033[1;35m")
        print(f.renderText("ExoAIO"))
        print(f"\t\t\t  \033[94m* Version: Beta - {VERSION}")
        print("\033[0m")
        print()

        taskManager = TaskManager(self.settings)
        loadTasks = taskManager.loadTasks()

        print(f"  \033[94m* [!] Loaded {len(loadTasks['All Tasks'])} Task(s)")
        
        proxyLists = taskManager.loadProxies()

        print(f"  \033[94m* [!] Loaded {len(proxyLists)} Proxy List(s)")

        print()


        options = loadTasks['Display']
        options.append('Start Captcha Bank')
        options.append('Configure Settings')
        options.append('Exit')

        questions = [
            inquirer.List('Option',
                          message="Selection",
                          choices=options,
                          ),
        ]

        answer = inquirer.prompt(questions, theme=UITheme())

        self.cls()
        
        pages = {
            'Start Captcha Bank':self.configureCaptchaBank,
            'Configure Settings':self.configureSettings,
            'Exit':sys.exit
        }

        if answer['Option'] in pages.keys():
            pages[answer['Option']]()
        else:
            allTasks = loadTasks['Options'][loadTasks['Display'].index(answer['Option'])]
            taskManager.startTasks(allTasks, proxyLists)

    def configureCaptchaBank(self):
        self.cls()

        sites = {
            'Stress95': {'SiteKey':'6LfSdnwUAAAAAF6vZ9LbeVbMCZNcTiw3VGdBK_Y9', 'URL':'https://stress95.com/', 'version':'v2', 'invisible':'0'},
            'NakedCPH': {'SiteKey':'6LeNqBUUAAAAAFbhC-CS22rwzkZjr_g4vMmqD_qo', 'URL':'https://www.nakedcph.com/', 'version':'v2', 'invisible':'1'},
            'SNS': {'SiteKey':'6LeKIW0UAAAAAA-ouoKHOnWuQDNymSwDFYeGP323', 'URL':'https://www.sneakersnstuff.com/', 'version':'v2', 'invisible':'1'},
            'YMEUniverse': {'SiteKey':'6LetlZQUAAAAAGkLxjR5zvrHZHOSlSFp6t-mrv6J', 'URL':'https://www.ymeuniverse.com/', 'version':'v2', 'invisible':'1'}
        }

        questions = [
            inquirer.List('Option',
                          message="Please Select A Site",
                          choices=['Stress95', 'NakedCPH', 'SNS', 'YMEUniverse'],
                          ),
        ]

        captchaBankSite = inquirer.prompt(questions, theme=UITheme())['Option']
        captchaBankSiteKey = sites[captchaBankSite]['SiteKey']
        captchaBankURL = sites[captchaBankSite]['URL']
        captchaBankVersion = sites[captchaBankSite]['version']
        captchaBankInvisible = sites[captchaBankSite]['invisible']

        self.cls()

        solvers = {
            '2Captcha':TwoCaptcha
        }

        questions = [
            inquirer.List('Option',
                          message="Please Select A Solving Service",
                          choices=['2Captcha'],
                          ),
        ]

        solverService = inquirer.prompt(questions, theme=UITheme())['Option']
        solver = solvers[solverService](self.settings[solverService])

        self.cls()

        Harvester(captchaBankSiteKey, captchaBankURL, captchaBankSite, captchaBankVersion, solver, captchaBankInvisible)

    def loadSettings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
                f.close()
        except:
            print(colored('Error Loading Settings!', 'red'))
            time.sleep(10)
            sys.exit()

    def configureSettings(self):
        settings = [
            'Webhook',
            '2Captcha'
        ]

        options = []

        for setting in settings:
            settingsOption = f'{setting} - {self.settings.setdefault(setting, "")}'
            options.append(settingsOption[:50] + (settingsOption[50:] and '...'))

        options.append('Back To Menu')

        questions = [
            inquirer.List('Option',
                          message="Please Select A Setting",
                          choices=options,
                          ),
        ]

        answer = inquirer.prompt(questions, theme=UITheme())

        if answer['Option'] == 'Back To Menu':
            self.menu()
        else:
            updateValue = settings[options.index(answer['Option'])]
            newValue = input('Please Enter New Value: ')

            try:
                with open('settings.json', 'r') as f:
                    data = json.loads(f.read())
                    data[updateValue] = newValue
                    self.settings[updateValue] = newValue
                    f.close() 

                with open('settings.json', 'w') as f:
                    json.dump(data, f, indent=2)
                    f.close()
            except:
                print(colored('Error Updating Settings!', 'red'))
                time.sleep(10)
                sys.exit()

            self.configureSettings()


if __name__ == '__main__':
    Main()
