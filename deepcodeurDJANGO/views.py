from django.http import HttpResponse

def home ():
    return render((request, 'DeepCodeur.html'))
