import json
import requests

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)


class Backend:
    base_url = config_data["backend_settings"]["base_url"]

    def post(self, relative_url, data):
        requests.post(f"{self.base_url}{relative_url}", json=data)


backend = Backend()
