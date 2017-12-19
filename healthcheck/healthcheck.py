try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

import traceback

from django.conf import settings
from django.db import connections
from django.core.cache import caches

import redis


def health_check_celery():
    """
    Check health status of celery and redis broker
    :return:
    """
    try:
        from celery import Celery
        app = Celery("health_check")
        app.config_from_object("django.conf:settings")
        stats = app.control.inspect().stats()
        if not stats:
            return False, "No running celery workers were found.", ''
    except Exception as e:
        return False, str(e), traceback.format_exc()
    return True, "Celery OK.", ''


def health_check_message_broker():
    """
    Check health status of message broker
    :return:
    """
    if hasattr(settings, 'BROKER_URL'):
        broker_url = settings.BROKER_URL
    else:
        broker_url = settings.broker_url

    url_obj = urlparse(broker_url)
    if url_obj.scheme == 'amqp':
        return ('Rabbitmq', ) + health_check_rabbitmq(broker_url)
    elif url_obj.scheme == 'redis':
        return ('Redis', ) + health_check_redis(url_obj.hostname,
                                                url_obj.port,
                                                url_obj.password)


def health_check_rabbitmq(broker_url):
    try:
        from kombu import Connection
        conn = Connection(broker_url)
        conn.connect()
        conn.release()
        return True, 'Rabbitmq is OK.', ''
    except Exception as e:
        return False, str(e), traceback.format_exc()


def health_check_db(connection):
    """
    Check health status of database.
    :return:
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True, "Database OK.", ''
    except Exception as e:
        return False, str(e), traceback.format_exc()


def health_check_databases():
    """
    Check health status of all databases configured
    """
    data = {}
    for conn in connections.all():
        ok, message, error = health_check_db(conn)
        data[conn.alias] = { "ok" : ok,
                             "message" : message,
                             "traceback" : error
                           }
    return data


def health_check_redis(hostname='127.0.0.1', port=6379,  password=''):
    """
    Check health status of redis server.
    :return:
    """
    try:
        r = redis.StrictRedis(host=hostname, port=port, password=password)
        r.set("Foo", "Bar")
        return True, "Redis server OK.", ''
    except Exception as e:
        return False, str(e), traceback.format_exc()


def health_check_salesforce():
    """
    Check health status of salesforce.
    :return:
    """
    from simple_salesforce import Salesforce
    try:
        if hasattr(settings, 'SANDBOX_MODE'):
            sandbox_mode = settings.SANDBOX_MODE
        else:
            sandbox_mode = True
        salesfroce = Salesforce(username=settings.SF_USERNAME,
                                password=settings.SF_PASSWORD,
                                security_token=settings.SF_TOKEN,
                                sandbox=sandbox_mode)
        sample_query = settings.SF_HC_QUERY
        accounts = salesfroce.query(sample_query)
        return True, "Salesforce is OK.", ''
    except Exception as e:
        return False, str(e), traceback.format_exc()


def health_check_cache(cache):
    """
    Check health status of a cache
    """
    try:
        cache.set('foo', 'bar', 30)
        if 'bar' != cache.get('foo'):
            return False, "Cache is not Ok", ""
        return True, 'Cache OK', ''
    except Exception as e:
        return False, str(e), traceback.format_exc()


def health_check_caches():
    """
    Check health status of all configured caches
    """
    data = {}
    cache_names = settings.CACHES
    for cache_name in cache_names:
        ok, message, error = health_check_cache(caches[cache_name])
        data[cache_name] = { 'ok' : ok,
                             'message' : message,
                             'error' : error
                           }
    return data

