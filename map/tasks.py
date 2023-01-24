# from django.core.mail import send_mail
#
# from config.celery import app
# from decouple import config
#
# from map.parsing import get_courses, get_soup, get_data
#
#
# @app.task
# def send_parsing():
#     html = get_courses(url=config('URL'))
#     soup = get_soup(html)
#     get_data(soup)

#
# @app.task
# def send_spam():
#     send_mail(
#         'Здравствуйте, Вас приветствует courses.kg',
#         'Мы рады что вы с нами!',
#         'artificialddemion@gmail.com',
#         'artificialddemion@gmail.com'
#     )
