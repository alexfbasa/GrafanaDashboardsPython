"""Overridden Low-level functions for building Grafana dashboards.
"""
import uuid

import attr
from attr.validators import instance_of
from grafanalib.core import Dashboard, Stat, STAT_TYPE
from grafanalib.core import Evaluator, is_valid_target


@attr.s
class RowPanel(object):
    title = attr.ib(validator=instance_of(str))
    collapsed = attr.ib(default=False, validator=instance_of(bool))
    panels = attr.ib(default=attr.Factory(list), validator=instance_of(list))
    gridPos = attr.ib(default=None)
    id = attr.ib(default=None)

    def _iter_panels(self):
        return iter(self.panels)

    def _map_panels(self, f):
        return f(self)

    def to_json_data(self):
        return {
            "id": self.id,
            "collapsed": self.collapsed,
            "gridPos": self.gridPos,
            'panels': self.panels,
            "title": self.title,
            "type": "row"
        }


@attr.s
class StatMappingValue(object):
    mapValue = attr.ib(default="", validator=instance_of(str))
    text = attr.ib(default="", validator=instance_of(str))
    color = attr.ib(default="", validator=instance_of(str))
    index = attr.ib(default=None)

    def to_json_data(self):
        return {
            "type": "value",
            "options": {
                self.mapValue: {
                    "text": self.text,
                    "color": self.color,
                    "index": self.index
                }
            }
        }


@attr.s
class StatMappingRange(object):
    from_value = attr.ib(validator=instance_of(int))
    to_value = attr.ib(validator=instance_of(int))
    text = attr.ib(default="", validator=instance_of(str))
    color = attr.ib(default="", validator=instance_of(str))
    index = attr.ib(default=None)

    def to_json_data(self):
        return {
            "type": "range",
            "options": {
                "from": self.from_value,
                "to": self.to_value,
                "result": {
                    "text": self.text,
                    "color": self.color,
                    "index": self.index
                }
            }
        }


@attr.s
class StatMappingSpecial(object):
    match = attr.ib(default="", validator=instance_of(str))
    text = attr.ib(default="", validator=instance_of(str))
    color = attr.ib(default="", validator=instance_of(str))
    index = attr.ib(default=None)

    def to_json_data(self):
        return {
            "type": "special",
            "options": {
                "match": self.match,
                "result": {
                    "text": self.text,
                    "color": self.color,
                    "index": self.index
                }
            }
        }


@attr.s
class DashboardWrapper(object):
    dashboard = attr.ib(validator=instance_of(Dashboard))
    folderUid = attr.ib(validator=instance_of(str))
    overwrite = attr.ib(default=True, validator=instance_of(bool))
    message = attr.ib(default="", validator=instance_of(str))

    def to_json_data(self):
        return {
            "dashboard": self.dashboard,
            "overwrite": self.overwrite,
            "message": self.message,
            "folderUid": self.folderUid
        }


@attr.s
class AlertCondition(object):
    target = attr.ib(validator=is_valid_target)
    evaluator = attr.ib(validator=instance_of(Evaluator))
    operator = attr.ib()
    reducerType = attr.ib()

    def to_json_data(self):
        return {
            "evaluator": self.evaluator,
            "operator": {
                "type": self.operator
            },
            "query": {
                "params": [self.target.refId]
            },
            "reducer": {
                "type": self.reducerType
            }
        }


@attr.s
class PrometheusTarget(object):
    expression = attr.ib(default=None, validator=instance_of(str))

    def to_json_data(self):
        return {
            "expr": self.expression,
            "format": "time_series",
            "interval": "",
            "intervalFactor": 2,
            "intervalMs": 1000,
            "legendFormat": "",
            "maxDataPoints": 43200,
            "refId": "A",
            "step": 2
        }


@attr.s
class AlertRule(object):
    alertConditions = attr.ib()
    uid = attr.ib(default=None)
    folderUid = attr.ib(default=None, validator=instance_of(str))
    title = attr.ib(default=None, validator=instance_of(str))
    datasourceUid = attr.ib(default=None, validator=instance_of(str))
    message = attr.ib(default=None, validator=instance_of(str))
    dashboardUid = attr.ib(default="", validator=instance_of(str))
    for_interval = attr.ib(default="5m", validator=instance_of(str))
    panelUid = attr.ib(default=None, validator=instance_of(str))
    target = attr.ib(default=None, validator=instance_of(object))
    openshiftUrl = attr.ib(default=None)
    kibanaUrl = attr.ib(default=None)
    fixGuideUrl = attr.ib(default=None)

    def get_uid(self):
        if self.uid is None:
            self.uid = f"{uuid.uuid4()}".replace("-", "")[:9]
        return self.uid

    def to_json_data(self):
        json_data = {
            "uid": self.get_uid(),
            "orgID": 1,
            "folderUID": self.folderUid,
            "ruleGroup": f"group-{self.folderUid}",
            "title": f"[{self.get_uid()}] {self.title}"[:190],
            "condition": "B",
            "data": [
                {
                    "refId": "A",
                    "queryType": "",
                    "relativeTimeRange": {
                        "from": 300,
                        "to": 0
                    },
                    "datasourceUid": self.datasourceUid,
                    "model": self.target
                },
                {
                    "refId": "B",
                    "queryType": "",
                    "relativeTimeRange": {
                        "from": 0,
                        "to": 0
                    },
                    "datasourceUid": "-100",
                    "model": {
                        "conditions": self.alertConditions,
                        "expression": "A",
                        "intervalMs": 1000,
                        "maxDataPoints": 43200,
                        "refId": "B",
                        "type": "classic_conditions"
                    }
                }
            ],
            "noDataState": "Alerting",
            "execErrState": "Alerting",
            "for": self.for_interval,
            "annotations": {
                "message": self.message,
                "__dashboardUid__": self.dashboardUid,
                "__panelId__": self.panelUid
            },
            "labels": {
                "rule_uid": self.get_uid(),
                "dashboard_uid": self.dashboardUid
            }
        }
        if self.openshiftUrl is not None:
            json_data['annotations']["openshift_url"] = self.openshiftUrl

        if self.kibanaUrl is not None:
            json_data['annotations']["kibana_url"] = self.kibanaUrl

        if self.fixGuideUrl is not None:
            json_data['annotations']["fix_guide_url"] = self.fixGuideUrl

        return json_data


@attr.s
class NotificationPolicyRoute(object):
    receiver = attr.ib(validator=instance_of(str))
    rule_uid = attr.ib(validator=instance_of(str))
    dashboard_uid = attr.ib(validator=instance_of(str))

    def to_json_data(self):
        return {
            "receiver": self.receiver,
            "object_matchers": [
                ["rule_uid", "=", self.rule_uid],
                ["dashboard_uid", "=", self.dashboard_uid]
            ]
        }


@attr.s
class TableOverride(object):
    matcher_id = attr.ib(validator=instance_of(str))
    matcher_options = attr.ib(validator=instance_of(str))
    property_id = attr.ib(validator=instance_of(str))
    property_value = attr.ib()

    def to_json_data(self):
        return {
            "matcher": {
                "id": self.matcher_id,
                "options": self.matcher_options
            },
            "properties": [
                {
                    "id": self.property_id,
                    "value": self.property_value
                }
            ]
        }


@attr.s
class TransformationGroupBy(object):
    fields = attr.ib(validator=instance_of(list))

    def to_json_data(self):
        json = {
            "id": "groupBy",
            "options": {
                "fields": {}
            }
        }
        for field in self.fields:
            json["options"]["fields"][field.name] = field
        return json


@attr.s
class TransformationField(object):
    name = attr.ib(validator=instance_of(str))
    operation = attr.ib(default=None)
    aggregations = attr.ib(default=[], validator=instance_of(list))

    def to_json_data(self):
        json = {
            "aggregations": self.aggregations
        }
        if self.operation is not None:
            json["operation"] = self.operation
        return json


@attr.s
class TransformationOrganize(object):
    field_names = attr.ib()

    def to_json_data(self):
        json = {
            "id": "organize",
            "options": {
                "excludeByName": {},
                "indexByName": {},
                "renameByName": {}
            }
        }
        for old_name, new_name in self.field_names.items():
            json["options"]["renameByName"][old_name] = new_name
        return json


@attr.s
class CustomStat(Stat):
    unit = attr.ib(default="none")
    color = attr.ib(default={
        "mode": "fixed",
        "fixedColor": "rgb(151, 31, 193)"
    })

    def to_json_data(self):
        return self.panel_json(
            {
                'fieldConfig': {
                    'defaults': {
                        'custom': {},
                        'decimals': self.decimals,
                        'mappings': self.mappings,
                        'unit': self.format,
                        'noValue': self.noValue,
                        'color': self.color
                    },
                    'overrides': self.overrides
                },
                'options': {
                    'textMode': self.textMode,
                    'colorMode': self.colorMode,
                    'graphMode': self.graphMode,
                    'justifyMode': self.alignment,
                    'orientation': self.orientation,
                    'reduceOptions': {
                        'calcs': [
                            self.reduceCalc
                        ],
                        'fields': self.fields,
                        'values': False
                    }
                },
                'type': STAT_TYPE,
            }
        )

