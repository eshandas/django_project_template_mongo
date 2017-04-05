import traceback
import json
import requests
import logging

from .models import (
    Log,
    RequestLog,
)
from .serializers import (
    LogSerializer,
    RequestLogSerializer,
)


class NoRequestException(Exception):
    pass


class NoExceptionException(Exception):
    pass


class NotLogObjException(Exception):
    pass


class NotRequestLogObjException(Exception):
    pass


class ObjectLogger(object):
    """
    The actual logger to log request, response and exception info.
    """
    def log_request(self, log=None, request=None, request_body=None):
        # -- General info
        log.request_url = request.get_full_path()
        log.request_method = request.method
        log.get_data = json.dumps(request.GET)
        log.request_body = request_body
        log.cookies = json.dumps(request.COOKIES)

        # --- Request meta info
        log.meta = ','.join('"%s": "%s"' % (k, str(v)) for k, v in request.META.items())
        log.meta = '{%s}' % log.meta
        log.meta = log.meta.replace('\\', '|')

        # --- User info
        if request.user is not None:
            if request.user.is_authenticated():
                log.user_id = request.user.id
                log.user_name = request.user.email

        # --- User agent info
        user_agent = request.user_agent
        # Browser
        log.request_browser = user_agent.browser
        # OS
        log.request_os = user_agent.os
        # Device
        log.request_device = user_agent.device
        # Device type
        log.is_mobile = user_agent.is_mobile
        log.is_tablet = user_agent.is_tablet
        log.is_touch_capable = user_agent.is_touch_capable
        log.is_pc = user_agent.is_pc
        log.is_bot = user_agent.is_bot

        return log

    def log_response(self, log, data, status=None, template_name=None, headers=None, content_type=None):
        log.response_body = json.dumps(data)
        log.response_status = status if status else 'None'
        log.response_headers = json.dumps(headers)
        log.response_content_type = content_type if content_type else 'None'

        return log

    def log_exception(self, log=None, exception=None):
        # --- Exception info
        log.exception_type = type(exception).__name__
        log.message = exception.message
        log.stack_trace = traceback.format_exc()

        return log

    def save_log(self, log=None, log_level=Log.INFO):
        if type(log) == Log:
            log.save()
            serializer = LogSerializer(log)
            logger = logging.getLogger('loggly_logs')
            if log_level == Log.ERROR:
                logger.error(serializer.data)
            elif log_level == Log.DEBUG:
                logger.debug(serializer.data)
            elif log_level == Log.WARN:
                logger.warn(serializer.data)
            elif log_level == Log.INFO:
                logger.info(serializer.data)
        else:
            raise NotLogObjException('Object passed is not a Log object')
        return log


class Logger(object):
    """
    Static methods to call underlying Logger without instantiating the class
    """
    @staticmethod
    def log_error(request=None, request_body=None, exception=None):
        if request and exception:
            log = Log(
                log_level=Log.ERROR)
            obj_logger = ObjectLogger()
            log = obj_logger.log_exception(log, exception)
            log = obj_logger.log_request(log, request, request_body)

            # --- Save
            log = obj_logger.save_log(log, Log.ERROR)
        elif request is None:
            raise NoRequestException('No http request found')
        elif exception is None:
            raise NoExceptionException('No exception found')

        return log

    @staticmethod
    def log_debug(request=None, message=None):
        stack_trace = ''.join(line for line in traceback.format_stack())
        message = message if message else ""
        if request:
            # -- General info
            log = Log(
                log_level=Log.DEBUG,
                message=message,
                stack_trace=stack_trace)
            obj_logger = ObjectLogger()
            log = obj_logger.log_request(log, request, request.body)

            # --- Save
            log = obj_logger.save_log(log, Log.DEBUG)
            return log
        else:
            raise NoRequestException('No http request found')

    @staticmethod
    def log_warn(request=None, message=None):
        stack_trace = ''.join(line for line in traceback.format_stack())
        message = message if message else ""
        if request:
            # -- General info
            log = Log(
                log_level=Log.WARN,
                message=message,
                stack_trace=stack_trace)
            obj_logger = ObjectLogger()
            log = obj_logger.log_request(log, request, request.body)

            # --- Save
            log = obj_logger.save_log(log, Log.WARN)
            return log
        else:
            raise NoRequestException('No http request found')

    @staticmethod
    def log_info(request=None, message=None):
        stack_trace = ''.join(line for line in traceback.format_stack())
        message = message if message else ""
        if request:
            # -- General info
            log = Log(
                log_level=Log.INFO,
                message=message,
                stack_trace=stack_trace)
            obj_logger = ObjectLogger()
            log = obj_logger.log_request(log, request, request.body)

            # --- Save
            log = obj_logger.save_log(log, Log.INFO)
            return log
        else:
            raise NoRequestException('No http request found')


class RequestObjectLogger(object):
    """
    The actual logger to log Requests request and response.
    """
    def log_request(self, log, request, data):
        # --- Request data
        log.method = request.method
        log.url = request.url
        log.request_data = data if isinstance(data, str) else json.dumps(data)
        headers = {val[0]: val[1] for val in request.headers.items()}
        log.request_headers = json.dumps(headers)

        return log

    def log_response(self, log, response, user, message):
        # --- Response data
        log.response_text = response.text
        log.response_status = response.status_code
        log.response_reason = response.reason
        log.response_time = response.elapsed.microseconds / 1000

        # --- User data
        if user is not None:
            if user.is_authenticated():
                log.user_id = user.id
                log.user_name = user.email
        log.message = message if message else ''

        return log

    def save_log(self, log=None):
        if type(log) == RequestLog:
            log.save()
            serializer = RequestLogSerializer(log)
            logger = logging.getLogger('loggly_logs')
            logger.info(serializer.data)
        else:
            raise NotRequestLogObjException('Object passed is not a RequestLog object')


class RequestLogger(object):
    @staticmethod
    def get(url, params=None, user=None, message=None, **kwargs):
        response = requests.get(url, params=params, **kwargs)
        log = RequestLog()

        obj_logger = RequestObjectLogger()

        log = obj_logger.log_request(log, response.request, params)
        log = obj_logger.log_response(log, response, user, message)

        # --- Save
        obj_logger.save_log(log=log)

        return response

    @staticmethod
    def post(url, data=None, json=None, user=None, message=None, **kwargs):
        response = requests.post(url, data=data, json=None, **kwargs)
        log = RequestLog()

        obj_logger = RequestObjectLogger()

        log = obj_logger.log_request(log, response.request, data)
        log = obj_logger.log_response(log, response, user, message)

        # --- Save
        obj_logger.save_log(log=log)

        return response

    @staticmethod
    def put(url, data=None, json=None, user=None, message=None, **kwargs):
        response = requests.put(url, data=data, json=None, **kwargs)
        log = RequestLog()

        obj_logger = RequestObjectLogger()

        log = obj_logger.log_request(log, response.request, data)
        log = obj_logger.log_response(log, response, user, message)

        # --- Save
        obj_logger.save_log(log=log)

        return response

    @staticmethod
    def delete(url, user=None, message=None, **kwargs):
        response = requests.delete(url, **kwargs)
        log = RequestLog()

        obj_logger = RequestObjectLogger()

        log = obj_logger.log_request(log, response.request, None)
        log = obj_logger.log_response(log, response, user, message)

        # --- Save
        obj_logger.save_log(log=log)

        return response

    @staticmethod
    def patch(url, data=None, json=None, user=None, message=None, **kwargs):
        response = requests.patch(url, data=data, json=None, **kwargs)
        log = RequestLog()

        obj_logger = RequestObjectLogger()

        log = obj_logger.log_request(log, response.request, data)
        log = obj_logger.log_response(log, response, user, message)

        # --- Save
        obj_logger.save_log(log=log)

        return response

    @staticmethod
    def head(url, user=None, message=None, **kwargs):
        response = requests.head(url, **kwargs)
        log = RequestLog()

        obj_logger = RequestObjectLogger()

        log = obj_logger.log_request(log, response.request, None)
        log = obj_logger.log_response(log, response, user, message)

        # --- Save
        obj_logger.save_log(log=log)

        return response
