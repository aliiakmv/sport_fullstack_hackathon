from decouple import config

from applications.section.models import ParsingGym
from applications.section.parser import get_sports_sections_html, get_soup, get_data
from config.celery import app


@app.task
def save_data_to_db():
    ParsingGym.objects.all().delete()
    html = get_sports_sections_html(config('PARSING_URL'))
    soup = get_soup(html)
    data = get_data(soup)
    ParsingGym.objects.bulk_create(data)

