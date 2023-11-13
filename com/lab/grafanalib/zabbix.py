import attr
from attr.validators import instance_of

ZABBIX_TRIGGERS_TYPE = 'alexanderzobnin-zabbix-triggers-panel'

ZABBIX_QMODE_METRICS = 0
ZABBIX_QMODE_SERVICES = 1
ZABBIX_QMODE_TEXT = 2

ZABBIX_SLA_PROP_STATUS = {
    'name': 'Status',
    'property': 'status'}

ZABBIX_SLA_PROP_SLA = {
    'name': 'SLA',
    'property': 'sla'}

ZABBIX_SLA_PROP_OKTIME = {
    'name': 'OK time',
    'property': 'okTime'}

ZABBIX_SLA_PROP_PROBTIME = {
    'name': 'Problem time',
    'property': 'problemTime'}

ZABBIX_SLA_PROP_DOWNTIME = {
    'name': 'Down time',
    'property': 'downtimeTime',
}

ZABBIX_EVENT_PROBLEMS = {
    'text': 'Problems',
    'value': [1]}

ZABBIX_EVENT_OK = {
    'text': 'OK',
    'value': [0]}

ZABBIX_EVENT_ALL = {
    'text': 'All',
    'value': [0, 1]}

ZABBIX_TRIGGERS_SHOW_ALL = 'all triggers'
ZABBIX_TRIGGERS_SHOW_ACK = 'acknowledged'
ZABBIX_TRIGGERS_SHOW_NACK = 'unacknowledged'

ZABBIX_SORT_TRIGGERS_BY_CHANGE = {
    'text': 'last change',
    'value': 'lastchange',
}
ZABBIX_SORT_TRIGGERS_BY_SEVERITY = {
    'text': 'severity',
    'value': 'priority',
}

ZABBIX_SEVERITY_COLORS = (
    ('#B7DBAB', 'Not classified'),
    ('#82B5D8', 'Information'),
    ('#E5AC0E', 'Warning'),
    ('#C15C17', 'Average'),
    ('#BF1B00', 'High'),
    ('#890F02', 'Disaster'),
)


@attr.s
class ZabbixTargetOptions(object):
    showDisabledItems = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'showDisabledItems': self.showDisabledItems
        }


@attr.s
class ZabbixTargetField(object):
    filter = attr.ib(default="", validator=instance_of(str))

    def to_json_data(self):
        return {
            'filter': self.filter
        }


@attr.s
class ZabbixTarget(object):
    """Generates Zabbix datasource target JSON structure.

    Grafana-Zabbix is a plugin for Grafana allowing
    to visualize monitoring data from Zabbix and create
    dashboards for analyzing metrics and realtime monitoring.

    Grafana docs on using Zabbix plugin: https://alexanderzobnin.github.io/grafana-zabbix/

    :param application: zabbix application name
    :param expr: zabbix arbitary query
    :param functions: list of zabbix aggregation functions
    :param group: zabbix host group
    :param host: hostname
    :param intervalFactor: defines interval between metric queries
    :param item: regexp that defines which metric to query
    :param itService: zabbix it service name
    :param mode: query mode type
    :param options: additional query options
    :param refId: target reference id
    :param slaProperty: zabbix it service sla property.
        Zabbix returns the following availability information about IT service
        Status - current status of the IT service
        SLA - SLA for the given time interval
        OK time - time the service was in OK state, in seconds
        Problem time - time the service was in problem state, in seconds
        Down time - time the service was in scheduled downtime, in seconds
    :param textFilter: query text filter. Use regex to extract a part of
        the returned value.
    :param useCaptureGroups: defines if capture groups should be used during
        metric query
    """

    application = attr.ib(default="", validator=instance_of(str))
    expr = attr.ib(default="")
    functions = attr.ib(default=attr.Factory(list))
    group = attr.ib(default="", validator=instance_of(str))
    host = attr.ib(default="", validator=instance_of(str))
    intervalFactor = attr.ib(default=2, validator=instance_of(int))
    item = attr.ib(default="", validator=instance_of(str))
    itService = attr.ib(default="", validator=instance_of(str))
    mode = attr.ib(default=ZABBIX_QMODE_METRICS, validator=instance_of(int))
    options = attr.ib(default=attr.Factory(ZabbixTargetOptions),
                      validator=instance_of(ZabbixTargetOptions))
    refId = attr.ib(default="")
    slaProperty = attr.ib(default=attr.Factory(dict))
    textFilter = attr.ib(default="", validator=instance_of(str))
    useCaptureGroups = attr.ib(default=False, validator=instance_of(bool))
    resultFormat = attr.ib(default="")

    def to_json_data(self):
        obj = {
            'application': ZabbixTargetField(self.application),
            'expr': self.expr,
            'functions': self.functions,
            'group': ZabbixTargetField(self.group),
            'host': ZabbixTargetField(self.host),
            'intervalFactor': self.intervalFactor,
            'item': ZabbixTargetField(self.item),
            'mode': self.mode,
            'options': self.options,
            'refId': self.refId,
            'resultFormat': self.resultFormat,
        }
        if self.mode == ZABBIX_QMODE_SERVICES:
            obj['slaProperty'] = self.slaProperty,
            obj['itservice'] = {'name': self.itService}
        if self.mode == ZABBIX_QMODE_TEXT:
            obj['textFilter'] = self.textFilter
            obj['useCaptureGroups'] = self.useCaptureGroups
        return obj
