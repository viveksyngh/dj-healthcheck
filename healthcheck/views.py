import json

from django.shortcuts import render
from django.http.response import HttpResponse
from django.conf import settings

from . import healthcheck as hc

# Create your views here.

def health_check(request):
    """
    View which provides health status of running services.
    """
    response = {}
    if hasattr(settings, 'BROKER_URL') or hasattr(settings, 'broker_url'):
        ok, message, traceback = hc.health_check_celery()
        response["celery"] =  {
                                "celery": {
                                    "ok": ok,
                                    "message": message,
                                    "traceback": traceback
                                    }
                                }

        broker_type, ok, message, traceback = hc.health_check_message_broker()
        response["celery"] = {
                                broker_type: {
                                    "ok": ok,
                                    "message": message,
                                    "traceback": traceback
                                    }
                                }

    response["databases"] =  hc.health_check_databases()
    response["caches"] = hc.health_check_caches()

    response["others"] = {}
    if hasattr(settings, 'SF_USERNAME') and hasattr(settings, 'SF_PASSWORD') \
        and hasattr(settings, 'SF_TOKEN') and hasattr(settings,
                                                      'SF_HC_QUERY'):
        ok, message, traceback = hc.health_check_salesforce()
        response["others"] = {
                                "salesforce" : {
                                    "ok" : ok,
                                    "message" : message,
                                    "traceback": traceback
                                     }
                                }
    return HttpResponse(json.dumps(response), content_type="application/json")

