import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as Bs

from applications.section.models import ParsingGym

from geopy.geocoders import Nominatim


options = webdriver.ChromeOptions()
ua = UserAgent()
options.add_argument('--headless')
options.add_argument(f'user-agent={ua.chrome}')
options.add_argument('--disable-blink-features=AutomationControlled')


geolocator = Nominatim(user_agent='Gym')

def get_sports_sections_html(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    courses_list = driver.find_elements(By.CLASS_NAME, value='Nv2PK')

    while True:
        ActionChains(driver).move_to_element(courses_list[-1]).perform()

        # скроллит список до конца
        last_review = courses_list[-1]
        driver.execute_script('arguments[0].scrollIntoView(true);', last_review)

        courses_list = driver.find_elements(By.CLASS_NAME, value='Nv2PK')
        if last_review == courses_list[-1]:
            return driver.page_source


def get_soup(html):
    soup = Bs(html, 'lxml')
    return soup


def get_data(soup):
    time.sleep(1)
    sport_list = soup.find_all('div', class_='Nv2PK')
    data = []
    for sport in sport_list[:30]:
        try:
            image = sport.find('div', class_='FQ2IWe p0Hhde').find('img').get('src')
        except AttributeError:
            image = ''
        try:
            text = sport.text.split()
            text = ' '.join([i for i in text if i])
            text = text.split('·')
            title = text[0]
            address = text[2]
        except AttributeError:
            title = ''
            address = ''
        try:
            location = geolocator.geocode(address)
            coordinates = (location.latitude, location.longitude)
        except AttributeError:
            coordinates = '0'
        data.append(ParsingGym(title=title, address=address, coordinates=coordinates, image=image))
    return data
