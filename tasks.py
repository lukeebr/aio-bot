import time, csv, codecs, glob, inquirer, sys, os, json, threading, datetime
from utils import UITheme
from termcolor import colored
from inquirer import themes

from modules.stress95 import Stress95
from modules.nakedcph import NakedCPH
from modules.sneakersnstuff import SNS
from modules.ymeuniverse import YMEUniverse

class TaskManager:
    def __init__(self, settings):
        self.settings = settings
        
        self.tasks = {
            'All Tasks':[],
            'CSV File':{},
            'Site':{},
            'Display':[],
            'Options':[]
        }

        self.sites = {
            'Stress95': Stress95,
            'NakedCPH': NakedCPH,
            'SNS':SNS,
            'YMEUniverse':YMEUniverse
        }


    def startTasks(self, allTasks, proxyLists):
        self.tasks = []

        count = 0

        taskData = {}

        for task in allTasks:
            if task['Proxy File'].strip() == '':
                proxies = []
            else:
                try:
                    proxies = proxyLists[task['Proxy File']]
                except:
                    print(colored(f'Error Loading Proxies From {task["Proxy File"]}', 'red'))
                    proxies = []
                    
            newTask = threading.Thread(target=self.sites[task['Site']], args=(task, proxies, count, self.settings, taskData,))
            self.tasks.append(newTask)
            count += 1

        print(colored(f'Starting {str(count)} Task(s)...', 'yellow'))

        for thread in self.tasks:
            thread.start()

        input()

    def loadProxies(self):
        proxyFiles = glob.glob('*.txt')
        proxyLists = {}
        for txt in proxyFiles:
            try:
                proxies = open(txt, 'r').read().splitlines()
                proxyLists[txt] = proxies
            except:
                pass
        return proxyLists
            

    def loadTasks(self):
        taskFiles = glob.glob('tasks*.csv')
        for csv in taskFiles:
            self.loadFromFile(csv)
        if len(self.tasks['All Tasks']) == 0:
            return
        else:
            self.tasks['Display'].append('Start All Tasks ' + ' ' * (35 - len('Start All Tasks ')) + '[' + str(len(self.tasks["All Tasks"])) + ' ' * (5 - len(str(len(self.tasks["All Tasks"])))) + ' Tasks]')
            self.tasks['Options'].append(self.tasks['All Tasks'])

        if len(self.tasks['CSV File']) != 0:
            for file in self.tasks['CSV File']:
                self.tasks['Display'].append(f'Start Tasks From CSV: {file} ' + ' ' * (35 - len(f'Start Tasks From CSV: {file} ')) + '[' + str(len(self.tasks["CSV File"][file])) + ' ' * (5 - len(str(len(self.tasks["CSV File"][file])))) + ' Tasks]')
                self.tasks['Options'].append(self.tasks['CSV File'][file])

        if len(self.tasks['Site']) != 0:
            for site in self.tasks['Site']:
                self.tasks['Display'].append(f'Start {site} Tasks ' + ' ' * (35 - len(f'Start {site} Tasks ')) + '[' + str(len(self.tasks["Site"][site])) + ' ' * (5 - len(str(len(self.tasks["Site"][site])))) + ' Tasks]')
                self.tasks['Options'].append(self.tasks['Site'][site])

        return self.tasks

    def loadFromFile(self, file):
        with codecs.open(file, 'r', 'utf-8') as f:
            tasks = []
            readCSV = csv.reader(f, delimiter=',')
            next(readCSV)
            for row in readCSV:
                try:
                    profile = {
                        'Site':row[0],
                        'Proxy File':row[1],
                        'Profile Name':row[2],
                        'Link': row[3],
                        'Size': row[4],
                        'Delay':row[5],
                        'Payment':row[6],
                        'Tasks':row[7]
                    }

                    if profile['Site'].lower().strip() in (k.lower() for k in self.sites):
                        profile['Site'] = (list(self.sites)[list(k.lower() for k in self.sites).index(profile['Site'].lower().strip())])
                        profile['Profile'] = self.loadProfile(profile['Profile Name'])
                        self.tasks['All Tasks'].extend(profile for x in range(int(profile['Tasks'])))
                        self.tasks['CSV File'].setdefault(file, []).extend(profile for x in range(int(profile['Tasks'])))
                        self.tasks['Site'].setdefault(profile['Site'], []).extend(profile for x in range(int(profile['Tasks'])))
                except:
                    continue
            f.close()

    def loadProfile(self, profile_name):
        with codecs.open('profiles.csv', 'r', 'utf-8') as f:
            readCSV = csv.reader(f, delimiter=',')
            next(readCSV)
            for row in readCSV:
                if row[0] == profile_name:
                    profile = {
                        'Address': row[1],
                        'City': row[2],
                        'Email': row[3],
                        'Password':row[4],
                        'First Name': row[5],
                        'Last Name': row[6],
                        'Phone': row[7],
                        'ZIP': row[8],
                        'Country': row[9],
                        'State':row[10]
                    }
                    
                    return profile
            raise Exception
