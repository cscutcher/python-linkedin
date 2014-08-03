# -*- coding: utf-8 -*-
import requests
from .exceptions import LinkedInError, get_exception_for_error_code


try:
    import simplejson as json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import json


def enum(enum_type='enum', base_classes=None, methods=None, **attrs):
    """
    Generates a enumeration with the given attributes.
    """
    # Enumerations can not be initalized as a new instance
    def __init__(instance, *args, **kwargs):
        raise RuntimeError('%s types can not be initialized.' % enum_type)

    if base_classes is None:
        base_classes = ()

    if methods is None:
        methods = {}

    base_classes = base_classes + (object,)
    for k, v in methods.items():
        methods[k] = classmethod(v)

    attrs['enums'] = attrs.copy()
    methods.update(attrs)
    methods['__init__'] = __init__
    return type(enum_type, base_classes, methods)


def raise_for_error(response):
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        try:
            error_info = response.json()
        except:
            error_info = {
                'status': response.status_code,
                'timestamp': 0,
                'errorCode': -1,
                'message': 'Unable to decode LinkedIn error response'}

        exception_type = get_exception_for_error_code(error_info['status'])
        message = '[%s:%s] %s' % (
            error_info['status'],
            error_info['errorCode'],
            error_info['message'])
        raise exception_type(message)
    except requests.ConnectionError as error:
        raise LinkedInError(repr(error))

HTTP_METHODS = enum('HTTPMethod', GET='GET', POST='POST',
                    PUT='PUT', DELETE='DELETE', PATCH='PATCH')
