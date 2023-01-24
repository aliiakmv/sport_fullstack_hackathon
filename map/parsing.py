import geocoder

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as Bs

from map.models import ParsingGym

options = webdriver.ChromeOptions()
ua = UserAgent()
options.add_argument('--headless')
options.add_argument(f'user-agent={ua.chrome}')
options.add_argument('--disable-blink-features=AutomationControlled')


def get_courses(url):
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
            print(driver.page_source)
            return driver.page_source


def get_soup(html):
    soup = Bs(html, 'lxml')
    return soup


def get_data(soup):
    sport_list = soup.find_all('div', class_='Nv2PK')
    data = []
    for sport in sport_list[:20]:
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
            g = geocoder.mapbox(address,
                                key='pk.eyJ1IjoiYW1vbnlhIiwiYSI6ImNsZDFkZmtibDBiZXczbm1wMWNmaXNtNDgifQ.zdiIZ8oySKdSFYwcpPs-uQ')
            g = g.latlng
            coordinate_lat = g[0]
            coordinate_long = g[1]
        except AttributeError:
            coordinate_lat = ''
            coordinate_long = ''
        data.append(
            ParsingGym(title=title, address=address, coordinate_lat=coordinate_lat, coordinate_long=coordinate_long,
                       image=image))
    return
