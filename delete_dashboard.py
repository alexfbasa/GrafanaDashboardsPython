from com.kn.monitoring.GrafanaClient import GrafanaClient
from com.kn.monitoring.util.Util import log_info, require_env

dashboard_uid = require_env("DASHBOARD_UID")

log_info(f"Deleting Dashboard, its alert rules and notification policies by uid: {dashboard_uid}]")
client = GrafanaClient()
client.delete_policies_and_alert_rules_by_dashboard_uid(dashboard_uid)
client.delete_dashboard(dashboard_uid)
log_info(f"Dashboard deleted successfully")
