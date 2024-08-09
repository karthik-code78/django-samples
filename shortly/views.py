from django.shortcuts import render
from django.http import HttpResponse
import pyshorteners

from shortly.forms import shortly_form


# Create your views here.
def shortener(request):
    if request.method == 'POST':
        form = shortly_form(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('url_field')
            print(type(url))
            if isinstance(url, bytes):
                url = url.decode('utf-8')
            print("url is: " + url)
            s = pyshorteners.Shortener()
            try:
                shortened_url = s.tinyurl.short(url)  # or another shortening service
                print("Shortened URL:", shortened_url)
            except Exception as e:
                print("Error shortening URL:", e)
    else:
        form = shortly_form()
    return render(request, 'shortly_form_template.html', {'shortly_form': form, 'shortened_url': shortened_url})
