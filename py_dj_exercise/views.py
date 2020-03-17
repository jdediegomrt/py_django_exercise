import logging
import requests

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_GET, require_safe

# @require_safe
# Web servers should automatically strip the content of responses to HEAD requests while leaving the headers unchanged,
# so you may handle HEAD requests exactly like GET requests in your views. Since some software, such as link checkers,
# rely on HEAD requests, you might prefer using require_safe instead of require_GET


@require_GET
def root(request):
    try:
        domain = request.GET.get('dominio')
        if not domain:
            return HttpResponseBadRequest('Missing required parameter: dominio')

        custom_ip = request.GET.get('ip')
        try:
            if custom_ip:
                custom_ip_port = request.GET.get('port')
                if custom_ip_port:
                    proxy = dict(
                            http='http://' + custom_ip + ':' + custom_ip_port,
                            https='https://' + custom_ip + ':' + custom_ip_port)
                else:
                    # assuming server hasn't port forwarding
                    proxy = dict(
                            http='http://' + custom_ip,
                            https='https://' + custom_ip)

                domain_request = requests.get(
                    'http://' + domain,
                    proxies=proxy)
            else:
                domain_request = requests.get('http://' + domain)
        except Exception as ex:
            logging.error('ERROR --> ', exc_info=ex)
            return JsonResponse(
                {
                    'status': 500,
                    'exception': str(ex)
                })

        logging.warning('domain_request TIME: ' + str(domain_request.elapsed.microseconds))
        logging.warning('domain_request CONTENT: ' + str(domain_request.content))
        logging.warning('domain_request URL: ' + str(domain_request.url))

        return JsonResponse(
            {
                'status': domain_request.status_code,
                'time': str(int(domain_request.elapsed.microseconds / 1000)) + 'ms'
            })

    except Exception as ex:
        logging.error('ERROR --> ', exc_info=ex)
        return HttpResponseServerError(ex)
