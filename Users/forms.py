from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from datetime import date,datetime
import hashlib
from django_otp.forms import OTPAuthenticationForm

def get_hash(string):
    hash_value = hashlib.sha256(string.encode()) 
    return hash_value.hexdigest()

class OTPAuthentication(OTPAuthenticationForm):
    otp_device = forms.CharField(required=False, widget=forms.HiddenInput)
    otp_challenge = forms.CharField(required=False, widget=forms.HiddenInput)
    otp_token = forms.CharField(required=False,max_length=6)  

def F(hash_value):
    last_char = hash_value[-1]
    new = hash_value[int(last_char,16):int(last_char,16)+7]
    otp = int(new,16)
    otp = int(str(otp)[0:4])
    return otp


def generate_OTP():
    hash_value = get_hash(str(datetime.now()))
    otp = F(hash_value)