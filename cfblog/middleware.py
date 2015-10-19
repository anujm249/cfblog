__author__ = 'vinay'
from django.conf import settings

from .models import Content
from .views import cms_page_index


class Middleware(object):

    def process_response(self, request, response):
        # ignore all ajax, static and media requests
        path = request.path_info
        if request.is_ajax() or \
                path.startswith(settings.STATIC_URL or '///') or \
                path.startswith(settings.MEDIA_URL or '///'):
            return response

        if response.status_code != 404:
            return response

        try:
            cms_page = Content.objects.get(url=path)
        except Content.DoesNotExist:
            return response
        else:
            return cms_page_index(request, cms_page=cms_page)
