from bs4 import BeautifulSoup as soup

my_url = 'https://www.doctolib.de/impfung-covid-19-corona/53115-bonn?ref_visit_motive_ids[]=6768&ref_visit_motive_ids[]=6936'

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import time
options = Options()
options.page_load_strategy = 'normal'
options.add_argument("--headless")
driver = webdriver.Chrome("/home/sali/Desktop/chromedriver", options=options)
driver.get(my_url)
delay = 3

height = driver.execute_script("return document.body.scrollHeight/10")
for i in range(10):
    driver.execute_script("window.scrollTo(0," + str(i*height) + ")")
    time.sleep(0.2)
page_html = driver.page_source
driver.close()
page_soup = soup(page_html, "lxml")
containers = page_soup.find_all("div", {"class":"dl-search-result"})

for container in containers:
    link = container.find('a', {"data-analytics-event-action":"bookAppointmentButton"}, href=True)['href']
    if container.find("div", {"class": "availabilities-empty-slot"}):
        print("yoo")
    if container.find("div", {"class": "Tappable-inactive"}):
        print(len(container.find_all("div", {"class": "Tappable-inactive"})), " appointments:")
        print("https://www.doctolib.de" + link)
