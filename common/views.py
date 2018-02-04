import logging

from pprint import pformat

from django.shortcuts import render


class ErrorView:
    @staticmethod
    def bad_request(request):
        logging.error('Bad Request. Request: %s', ErrorView.stringify(request))
        return render(request, 'error/error.html', {'code': 400, 'message': 'Bad Request'},
                      status=400)

    @staticmethod
    def permission_denied(request):
        logging.error('Permission Denied. Request: %s', ErrorView.stringify(request))
        return render(request, 'error/error.html', {'code': 403, 'message': 'Permission Denied'},
                      status=403)

    @staticmethod
    def page_not_found(request):
        logging.error('Not found. Request: %s', ErrorView.stringify(request))
        return render(request, 'error/error.html', {'code': 404, 'message': 'Not Found'},
                      status=404)

    @staticmethod
    def server_error(request):
        logging.error('Internal Error. Request: %s', ErrorView.stringify(request))
        return render(request, 'error/error.html', {'code': 500, 'message': 'Internal Error'},
                      status=500)

    @staticmethod
    def stringify(obj):
        return '<' + type(obj).__name__ + '> ' + pformat(vars(obj), indent=4, width=1)


logging.basicConfig(filename='app.log', level=logging.ERROR)
