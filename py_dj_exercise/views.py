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
            return HttpResponseBadRequest('Missing required parameter: domain')

        domain_request = requests.get('http://' + domain)
        logging.warning('domain_request TIME: ' + str(domain_request.elapsed.microseconds))

        return JsonResponse(
            {
                'status': domain_request.status_code,
                'time': str(int(domain_request.elapsed.microseconds / 1000)) + 'ms'
            })

    except Exception as e:
        logging.error('Error at %s', 'division', exc_info=e)
        return HttpResponseServerError(e)
