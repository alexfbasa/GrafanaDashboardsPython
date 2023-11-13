import time
from enum import IntEnum
from os import getenv

from com.lab.monitoring.exception.provisioning_exception import ProvisioningException

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class LogLevel(IntEnum):
    ERROR = 1
    INFO = 2
    DEBUG = 3


LOG_LEVEL = LogLevel.DEBUG


def log_debug(text):
    log(text, LogLevel.DEBUG)


def log_info(text):
    log(text, LogLevel.INFO)


def log_error(text):
    log(text, LogLevel.ERROR)


def log(text, level: LogLevel):
    if level <= LOG_LEVEL:
        print(f"[{time.strftime(DATE_TIME_FORMAT)}] {level.name} - {text}")


def default_if_none(value, default_value):
    return value if value is not None else default_value


def query_by_pod(service_name):
    return " AND ".join(f"pod:{v}" for v in service_name.split("-"))


def query_by_elasticsearch(elasticsearch_name):
    return f"{elasticsearch_name}-{elasticsearch_name}.*"


def require_env(var_name):
    value = getenv(var_name)
    if value is None:
        raise ProvisioningException(f"Environment Variable '{var_name}' is not specified")
    return value
