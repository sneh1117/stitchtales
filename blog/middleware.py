import requests
from django.conf import settings


EXCLUDED_PATHS=[
    '/admin/',
    '/static/',
    '/media/',
    '/favicon/',
    '/robots.txt',
    '/sitemap',
]

EXCLUDED_IPS=getattr(settings,'ANALYTICS_EXCLUDED_IPS',[])


def get_client_ip(request):
    x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR','')


def get_location(ip):
    try:
        response=requests.get(f'http://ip-api.com/json/{ip}?fields=country,city',timeout=2)
        if response.status_code==200:
            data=response.json()
            return data.get('country',''),data.get('city','')
    except Exception:
        pass
    return '',''


class VisitorTrackingMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response


    def __call__(self,request):
        response=self.get_response(request)


        if request.method != 'GET':
            return response
        
        path =request.path

        if any(path.startswith(p) for p in EXCLUDED_PATHS):
            return response
        

        ip= get_client_ip(request)


        if ip in EXCLUDED_IPS:
            return response
        
        if request.user.is_authenticated and (request.user.is_staff or  request.user.is_superuser):
            return response
        

        try:
             from .models import Visitor
             referrer=request.META.get('HTTP_REFERER','')
             user_agent=request.META.get('HTTP_USER_AGENT','')
             country, city=get_location(ip)


             Visitor.objects.create(
                 ip_address=ip,
                 path=path,
                 referrer=referrer[:500] if referrer else '',
                 country=country,
                 city=city,
                 user_agent=user_agent[:500],
                 is_authenticated=request.user.is_authenticated,
             )
        except Exception:
            pass

        return response