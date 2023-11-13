dashboard_group = require_env("DASHBOARD_GROUP")

log_info(f"Provisioning Dashboards for group {dashboard_group}")
functions = {
    "PRJ01": provision_prj01_dashboards,
    "PRJ02": provision_prj02_dashboards,
    "PRJ03": provision_prj03_dashboards
}
functions[dashboard_group]()
log_info(f"Dashboard provisioned successfully")
