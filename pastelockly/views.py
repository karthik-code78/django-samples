import base64
from idlelib.iomenu import errors

import bcrypt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from djangoProject.settings import crypt_default_key
from pastelockly.forms import pastelockly_form
from pastelockly.models import PasteLock

# Create your views here.

IV = 16 * b'\x00'
BLOCK_SIZE = 32 # Bytes

# cache for 2 minutes
@cache_page(timeout=60 * 2)
def saveToDb(request):
    errors: [str] = []
    pastelockly_list = PasteLock.objects.all()
    if request.method == 'POST':
        form = pastelockly_form(request.POST)
        text=""
        is_locked = False
        pass_text = ""
        if form.is_valid():
            text = form.cleaned_data.get('text_field')
            is_locked = form.cleaned_data.get('is_locked')
            pass_text = form.cleaned_data.get('password_field')
            print(form.cleaned_data)
            if is_locked:
                print("is locked")
                if pass_text == "" or pass_text is None:
                    print("is_locked please provide password")
                    errors.append("view is locked please provide password")
                else:
                    print("password has been provided")
                    AES_obj = AES.new(pass_text.encode(), AES.MODE_ECB)
                    encrypted_text = AES_obj.encrypt(pad(text.encode(), BLOCK_SIZE))
                    text = base64.b64encode(encrypted_text).decode('utf-8')
                    print(text)
            else:
                print("is not locked")
            if len(errors) == 0:
                try:
                    pasteLock = PasteLock(
                        text_field=text,
                        password_field=pass_text,
                        is_locked=is_locked
                    )
                    pasteLock.save()
                    form = pastelockly_form()
                except Exception as e:
                    print("Error saving to db: ", e)
                    errors.append("Error saving to db")
    else:
        form = pastelockly_form()
    return render(request, 'pastelockly_form_template.html', {'pastelockly_list': pastelockly_list, 'pastelockly_form': form, 'errors': errors})

def getPaste(request, id):
    errors: [str] = []
    pasteLock = PasteLock.objects.get(id=id)
    if request.method == 'GET':
        text = pasteLock.text_field
        # # decoded_string = unpad(text, BLOCK_SIZE)
        # encrypted_text = base64.b64decode(pasteLock.text_field)
        # print(text)
        # pass_text = pasteLock.password_field
        # AES_obj = AES.new(pass_text.encode(), AES.MODE_ECB)
        # decrypted_text = unpad(AES_obj.decrypt(encrypted_text), BLOCK_SIZE).decode('utf-8')
        # print(decrypted_text)
        print(text)
    elif request.method == 'POST':
        text = request.POST.get('text_field')
        print(text)
        pass_text = request.POST.get('password_field')
        if pass_text != pasteLock.password_field:
            print("password doesn't match")
            errors.append("password doesn't match")
            return render(request, 'pastelockly_share_template.html', {'pasteLock': pasteLock, 'errors': errors})
        encrypted_text = base64.b64decode(text)
        AES_obj = AES.new(pass_text.encode(), AES.MODE_ECB)
        decrypted_text = unpad(AES_obj.decrypt(encrypted_text), BLOCK_SIZE).decode('utf-8')
        print(decrypted_text)
        pasteLock = PasteLock(
            text_field=decrypted_text,
            password_field=pass_text,
            is_locked=False
        )
    return render(request, 'pastelockly_share_template.html', {'pasteLock': pasteLock, 'errors': errors})