class ZabbixDatasource:
    def __init__(self, uid: str, name: str, type: str, url: str):
        self.uid: str = uid
        self.name: str = name
        self.type: str = type
        self.url: str = url


def from_json(json_data) -> ZabbixDatasource:
    return ZabbixDatasource(json_data['uid'], json_data['name'], json_data['type'], json_data['url'])
