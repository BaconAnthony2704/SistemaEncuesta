from django import forms
from captcha.fields import CaptchaField
from .models import *


#Clase para obtener la visualiacion del captcha, se hace en el form.py para luego solo llamarla
#en el template que desea ser invocada
class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()