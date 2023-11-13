import json
import requests

from grafanalib._gen import DashboardEncoder
from com.lab.grafanalib.core import DashboardWrapper, AlertRule
from com.lab.monitoring.exception.provisioning_exception import ProvisioningException
from com.lab.monitoring.model import ZabbixDatasource
from com.lab.monitoring.util.Util import log_debug, log_info, require_env, log_error


class GrafanaClient:

    def __init__(self):
        self.grafana_host = "https://your-grafana-ip"

        self.grafana_api_key = require_env("GRAFANA_API_KEY")

        self.headers = {'Authorization': f"Bearer {self.grafana_api_key}", 'Content-Type': 'application/json'}

    def post(self, url, json_data):
        resp = requests.post(f"{self.grafana_host}/{url}", data=json_data, headers=self.headers, verify=True)
        if resp.status_code == 500:
            log_error(f"Response: {resp.status_code} - {resp.content}")
        else:
            log_debug(f"Response: {resp.status_code} - {resp.content}")
        return resp

    def delete(self, url):
        resp = requests.delete(f"{self.grafana_host}/{url}", headers=self.headers, verify=True)
        log_debug(f"Response: {resp.status_code} - {resp.content}")
        return resp

    def get(self, url):
        resp = requests.get(f"{self.grafana_host}/{url}", headers=self.headers, verify=True)
        log_debug(f"Response: {resp.status_code} - {resp.content}")
        return resp

    def put(self, url, json_data):
        resp = requests.put(f"{self.grafana_host}/{url}", data=json_data, headers=self.headers, verify=True)
        log_debug(f"Response: {resp.status_code} - {resp.content}")
        return resp

    def save_dashboard(self, dashboard_wrapper: DashboardWrapper):
        log_info(f"Saving dashboard - {dashboard_wrapper.dashboard.title}")
        resp = self.post("api/dashboards/db", self.to_json_data(dashboard_wrapper))

        log_debug(f"{resp.status_code} - {resp.content}")
        if resp.status_code == 200:
            log_info(f"Dashboard uploaded successfully")
        else:
            raise ProvisioningException(f"Dashboard uploading failed")
        return json.loads(resp.content.decode('utf8'))

    def delete_dashboard(self, dashboard_uid):
        log_info(f"Deleting Dashboard [uid: {dashboard_uid}]")
        return self.delete(f"api/dashboards/uid/{dashboard_uid}")

    def find_datasources(self):
        log_info("Getting all Datasources")
        resp = self.get("api/datasources")
        return json.loads(resp.content.decode('utf8'))

    def find_zabbix_datasource(self) -> [ZabbixDatasource]:
        datasources = self.find_datasources()
        return [ZabbixDatasource.from_json(ds) for ds in datasources if
                ds['type'] == 'alexanderzobnin-zabbix-datasource']

    def add_alert_rule(self, alert_rule: AlertRule):
        log_info(f"Adding Alert Rule [uid: {alert_rule.get_uid()}]")
        return self.post("api/v1/provisioning/alert-rules", self.to_json_data(alert_rule))

    def delete_alert_rule(self, alert_rule_uid):
        log_info(f"Deleting Alert Rule [uid: {alert_rule_uid}]")
        return self.delete(f"api/v1/provisioning/alert-rules/{alert_rule_uid}")

    def delete_alert_rules(self, alert_rule_uids: [str]):
        for alert_rule_uid in alert_rule_uids:
            self.delete_alert_rule(alert_rule_uid)

    def get_notification_policies(self):
        resp = self.get("api/v1/provisioning/policies")
        return json.loads(resp.content.decode('utf8'))

    def add_notification_policy_routes(self, routes):
        policies = self.get_notification_policies()
        policies["routes"] += routes
        return self.save_notification_policies(policies)

    def save_notification_policies(self, policies):
        log_info("Saving notification policies")
        return self.put("api/v1/provisioning/policies", self.to_json_data(policies))

    def delete_policies_and_alert_rules_by_dashboard_uid(self, dashboard_uid):
        policies = self.get_notification_policies()
        new_routes = []
        alert_rule_uids_to_delete = []
        for route in policies["routes"]:
            if self.get_matcher_value(route, "dashboard_uid") == dashboard_uid:
                rule_uid = self.get_matcher_value(route, "rule_uid")
                alert_rule_uids_to_delete.append(rule_uid)
            else:
                new_routes.append(route)

        policies["routes"] = new_routes
        self.save_notification_policies(policies)
        self.delete_alert_rules(alert_rule_uids_to_delete)

    def find_contact_points(self):
        resp = self.get("api/v1/provisioning/contact-points")
        return json.loads(resp.content.decode('utf8'))

    def find_folders(self):
        resp = self.get("api/folders")
        return json.loads(resp.content.decode('utf8'))

    def to_json_data(self, obj) -> str:
        return json.dumps(obj, sort_keys=True, indent=2, cls=DashboardEncoder)

    def get_matcher_value(self, notification_policy_route, label):
        for matcher in notification_policy_route["object_matchers"]:
            if matcher[0] == label:
                return matcher[2]
        return None
