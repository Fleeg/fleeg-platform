import logging

from django.shortcuts import render


class ErrorView:
    @staticmethod
    def not_authorized(request):
        logging.error('Not Authorized. Request: %s', request)
        return render(request, 'error/error.html', {'code': 400, 'message': 'Not Authorized'},
                      status=400)

    @staticmethod
    def permission_denied(request):
        logging.error('Permission Denied. Request: %s', request)
        return render(request, 'error/error.html', {'code': 403, 'message': 'Permission Denied'},
                      status=403)

    @staticmethod
    def page_not_found(request):
        logging.error('Not found. Request: %s', request)
        return render(request, 'error/error.html', {'code': 404, 'message': 'Not Found'},
                      status=404)

    @staticmethod
    def server_error(request):
        logging.error('Internal Error. Request: %s', request)
        return render(request, 'error/error.html', {'code': 500, 'message': 'Internal Error'},
                      status=500)


logging.basicConfig(filename='app.log', level=logging.ERROR)
