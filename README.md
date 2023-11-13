# Grafana Dashboards

## About

This project provides Grafana Dashboards-as-a-Code for monitoring GIGD applications. The dashboards are described
using [Grafanalib](https://github.com/weaveworks/grafanalib), a Python library for building Grafana dashboards.

## Architecture

For a detailed understanding of the architecture, please refer to
our [Wiki](https://medium.com/@tarantool/grafana-as-code-b642cac9ae75).

## Prerequisites

Ensure you have the following prerequisites installed:

- Docker
- Python 3.9

You can install Python 3.9 using [Chocolatey](https://community.chocolatey.org/) with the command:

```shell
choco install python --version=3.9.0
```

## Environment Variables

The script utilizes the following environment variables:

- `DASHBOARD_GROUP`: Name of the dashboards group to be provisioned (e.g., `PRJ01`, `PRJ02`, `PRJ03`).
- `GRAFANA_API_KEY`: Authentication token for interacting with the Grafana API.
- `ALERT_RULES_PROVISIONING_ENABLED`: Set to either `True` or `False` to enable or disable the provisioning of alert
  rules and notification policies along with dashboard updates.

## Installation

Follow these steps to get started:

1. Clone the Git repository.
2. Install Python using [pip](https://pip.pypa.io/en/stable/installation/).
3. Download the required dependencies:

```shell
pip install -r requirements.txt
```

## Local Deployment

To deploy locally, define the required environment variables and execute the script:

```shell
export DASHBOARD_GROUP=<Specify group here>
export GRAFANA_API_KEY=<Specify API key here>
export ALERT_RULES_PROVISIONING_ENABLED=<Specify alerts provisioning here>
export PYTHONUNBUFFERED=1
python provision_dashboard.py
```

The script will create or update dashboards for the specified group in [Grafana](https://your-grafana-ip/).

## Deployment with Docker

To deploy using Docker, follow these steps:

1. Clone the Git repository.
2. Navigate to the cloned repository and build the Docker image:

```shell
docker build -t grafana-dashboards -f cicd/Dockerfile .
```

3. Provision dashboards for a given group:

```shell
docker run \
  -e DASHBOARD_GROUP=<Specify group here> \
  -e GRAFANA_API_KEY=<Specify API key here> \
  -e ALERT_RULES_PROVISIONING_ENABLED=True \
  -e PYTHONUNBUFFERED=1 \
  -v $(pwd):/app grafana-dashboards python provision_dashboard.py
```

## Jenkins Deployment

For deployment using Jenkins:

1. Open the [Jenkins Job](https://your-jenkins/view/project/job/provision_grafana-dashboards/).
2. Select the master branch.
3. Click `Build with Parameters`.
4. Choose the group from the dropdown list to provision dashboards.
5. Click `Build`.
6. Verify the dashboards in [Grafana](https://your-grafana-ip/).

## Deleting Dashboard by UID

To delete a dashboard by UID, define the required environment variables and execute the script:

```shell
export DASHBOARD_UID=<Specify dashboard UID here>
export GRAFANA_API_KEY=<Specify API key here>
export PYTHONUNBUFFERED=1
python delete_dashboard.py
```

The script will delete the specified dashboard, along with its alert rules and notification policies.

[//]: # ()

[//]: # (## Grafana Code Generator)

[//]: # ()

[//]: # (The application generates enumerations for Grafana ContactPoints, Folders, and Datasources. To run the script, execute:)

[//]: # ()

[//]: # (```shell)

[//]: # (export GRAFANA_API_KEY=<Specify API key here>)

[//]: # (python com/kn/generator/run.py)

[//]: # (```)

[//]: # ()

[//]: # (This will fetch folders, contact points, and datasources using the Grafana API and generate the enumeration files:)

[//]: # ()

[//]: # (- [ContactPoints.py]&#40;com/kn/monitoring/generated/ContactPoints.py&#41;)

[//]: # (- [Folders.py]&#40;com/kn/monitoring/generated/Folders.py&#41;)

[//]: # (- [ElasticsearchDatasources.py]&#40;com/kn/monitoring/generated/ElasticsearchDatasources.py&#41;)

[//]: # (- [PrometheusDatasources.py]&#40;com/kn/monitoring/generated/PrometheusDatasources.py&#41;)

[//]: # ()

[//]: # (Commit the generated files to reflect the changes.)

## Postman Collection

Use [Grafana_API.postman_collection.json](Grafana_API.postman_collection.json) to create/delete alerts and policies
through the [Grafana HTTP API](https://grafana.com/docs/grafana/latest/developers/http_api/).

To use the collection:

1. Install [Postman](https://www.postman.com/downloads/).
2. Import [Grafana_API.postman_collection.json](Grafana_API.postman_collection.json) into Postman.
3. In Postman, open the imported Grafana API collection, go to the Authorization tab, and specify the Bearer token.

Feel free to adjust the instructions based on your specific project requirements.