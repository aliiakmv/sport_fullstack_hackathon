import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible

from applications.payments import utils


@deconstructible
class CCNumberValidator:
    def __call__(self, value, *args, **kwargs):
        if not utils.luhn(utils.get_digits(value)):
            raise ValidationError('Enter a valid credit card number', code='invalid')


@deconstructible
class ExpiryDateValidator:
    def __call__(self, value, *args, **kwargs):
        expiry_date = utils.expire_date(value.year, value.month)
        if expiry_date < datetime.date.today():
            raise ValidationError('This date has passed', code='date_passed')
