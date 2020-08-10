import json
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import requests
import urllib


class Automate:
    site = 'https://jntuaresults.ac.in/'
    status = 'Invalid Hall Ticket Number for the Exam code you have selected.'

    def __init__(self, rollno) -> None:
        self.rollno = rollno

    @classmethod
    def connect(cls, host=site):
        ''' check for internet connection '''

        try:
            urllib.request.urlopen(host)
            return True
        except:
            return False

    @classmethod
    def getAllUrls(cls):
        '''
        get all b.tech r15 results links
        '''
        site = 'https://jntuaresults.ac.in/'
        src = requests.get(site).text
        soup = BeautifulSoup(src, 'lxml')
        # table = soup.find('table', {'class': 'ui table segment'})
        return [site+row['href'] for row in soup.findAll("a", href=True) if (("B.Tech" and "R15") in row.text) and ("B.Pharmacy" not in row.text)]

    @classmethod
    def submiCredentials(cls, driver, rollno, e):
        driver.get(e)
        field = driver.find_element_by_xpath(
            '/html/body/div/div[1]/div/div/center/table/tbody/tr/th/center/input[1]')
        btn = driver.find_element_by_xpath(
            '/html/body/div/div[1]/div/div/center/table/tbody/tr/th/center/input[2]')
        # print('enterning roll no')
        field.send_keys(rollno)
        # print('button click')
        btn.click()

        def waitForPageLoad():
            html = driver.page_source
            while True:
                # print('checking for  source')
                t = driver.page_source
                if html != t:
                    # print('source changed')
                    return 0

        # print('witing for loading')
        waitForPageLoad()
        # print('capturing screenshot')
        # driver.save_screenshot("images\\screenshot.png")
        return driver.page_source

    @classmethod
    def userDetails(cls, res):
        src = res
        soup = BeautifulSoup(src, 'lxml')
        user = {}
        for i in soup.findAll('b'):
            if i.text == 'Hall Ticket No :':
                t = {'Hall Ticket No': i.next_sibling[:10].upper()}
                user.update(t)
            elif i.text == 'Student name: ':
                t = {'Student name': i.next_sibling}
                user.update(t)
        return user

    @classmethod
    def userResults(cls, res):
        src = res
        soup = BeautifulSoup(src, 'lxml')
        headder = soup.find('h1', {'class': 'ui info message bxinfo'})
        table = soup.find('table', {'class': 'ui table segment'})
        resl = ['Subject Code', 'Subject Name',  'Internals', 'Externals',
                'Total Marks', 'Result Status', 'Credits', 'Grades']

        try:
            values = [i.text for i in table.findAll("td")]
            l = []
            _from = 0
            _to = 8
            for _ in range(len(values)//8):
                x = {}
                for i, j in zip(resl, values[_from:_to]):
                    x[i] = j
                _from += 8
                _to += 8
                l.append(x)
            data = {'title': headder.text.strip('Title : '), 'data': l}
            return data
        except:
            return {'title': headder.text.strip('Title : '), 'data': None}

    def getData(self, driver, urls):
        try:
            x = {}
            l = []
            userGoten = 0
            for i, e in enumerate(urls):
                print(len(urls) - i)
                res = Automate.submiCredentials(driver, self.rollno, e)
                if userGoten == 0:
                    ud = {'user': Automate.userDetails(res)}
                    if len(ud['user']) == 2:
                        x.update(ud)
                        userGoten += 1
                ur = Automate.userResults(res)
                if ur['data'] != None:
                    l.append(ur)
            x.update({'results': l})
            return x
        except Exception as e:
            return e

    def start(self):
        try:
            if Automate.connect():
                options = Options()
                options.headless = True
                driver = webdriver.Chrome(
                    executable_path='src\\chromedriver\\chromedriver.exe', options=options)
                urls = Automate.getAllUrls()
                data = self.getData(driver, urls)
                # print(data)
                try:
                    with open(f"src\\results\\{self.rollno}.json", 'w') as f:
                        f.write(json.dumps(data, indent=2))
                except Exception as e:
                    print(e)
                finally:
                    print('closing browser')
                    driver.quit()
                    return data
            else:
                print('No INternet')
        except Exception as e:
            print(e)
