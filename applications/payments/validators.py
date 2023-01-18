import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as gl

@deconstructible
class CCNumberValidator:
    def __init__(self, code):
        self.code = code

    def __call__(self, *args, **kwargs):
        if 