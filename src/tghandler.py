import traceback
import requests


class TGHandler:

    def __init__(self, get_response):
        self.ex_info = ''
        self.get_response = get_response

    def process_exception(self, request, exception):
        try:
            self.ex_info = ''.join(traceback.format_tb(exception.__traceback__))
        except  Exception:
            pass

    def __call__(self, req):
        from django.conf import settings
        host = settings.TG_HANDLER_HOST
        response = self.get_response(req)
        body = ''
        try:
            if 200 <= response.status_code < 400:
                return response

            res_code = response.status_code
            reason_phrase = response.reason_phrase
            if response.headers['Content-type'] == 'application/json':
                body = response.content.decode()

            data = {
                'error': {
                    'res_code': res_code,
                    'reason': reason_phrase,
                    'body': body,
                    'ex_info': self.ex_info
                },
                'code': settings.TG_HANDLER_CODE
            }

            requests.post(f'http://{host}/handle/', json=data)
        except Exception:
            pass

        return response

