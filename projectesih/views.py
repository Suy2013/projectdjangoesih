from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import datetime


def home(request):
    return HttpResponse("Hello world merde")
def help(request):
    return HttpResponse("Help me please")
def current_datetime(request):
    now = datetime.datetime.now()
    dic = {'current_date': now,'name': 'Suy Emmanuel','residence': 'Port-au-Prince','age': 25, 'detail':'Je suis d\'une famille de 8 enfants avec un pere et une mere honnete et genereuse'}
    t = get_template('current_datetime.html')
    html = t.render(Context(dic))
    return HttpResponse(html)
