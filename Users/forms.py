from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from datetime import date,datetime
import hashlib


def get_hash(string):
    hash_value = hashlib.sha256(string.encode()) 
    return hash_value.hexdigest()

class OTPAuthenticationForm(AuthenticationForm):
    otp = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean(self):
        super(OTPAuthenticationForm, self).clean()
        if otp != '1234':
            raise forms.ValidationError("Enter OTP you received via e-mail")

        if self.request.session.has_key('_otp'):
            if self.request.session['_otp'] != self.cleaned_data['otp']:
                raise forms.ValidationError("Invalid OTP.")
            del self.request.session['_otp']
        else:
            otp = '1234'
            print(otp)
            send_mail(
                subject="Your OTP Password",
                message="Your OTP password is %s" % otp,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.user_cache.email]
            )
            self.request.session['_otp'] = otp
            raise forms.ValidationError("Enter OTP you received via e-mail")

def F(hash_value):
    last_char = hash_value[-1]
    new = hash_value[int(last_char,16):int(last_char,16)+7]
    otp = int(new,16)
    otp = int(str(otp)[0:4])
    return otp


def generate_OTP():
    hash_value = get_hash(str(datetime.now()))
    otp = F(hash_value)