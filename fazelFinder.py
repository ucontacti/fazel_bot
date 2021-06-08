from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time

result = []
def fazelFinder(my_url = 'https://www.doctolib.de/impfung-covid-19-corona/53115-bonn?ref_visit_motive_ids[]=6768&ref_visit_motive_ids[]=6936'):    

    options = Options()
    options.page_load_strategy = 'normal'
    options.add_argument("--headless")
    driver = webdriver.Chrome("/home/sali/Desktop/chromedriver", options=options)
    driver.get(my_url)

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
        if container.find("div", {"class": "Tappable-inactive"}):
            no_appointment = len(container.find_all("div", {"class": "Tappable-inactive"}))
            doc_link = "https://www.doctolib.de" + link
            result.append([no_appointment, doc_link])            
    return result

