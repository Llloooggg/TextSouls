import json
import requests

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)


class Backend:
    base_url = config_data["BACKEND_SETTINGS"]["BASE_URL"]

    def post(self, relative_url, data):
        try:
            response = requests.post(
                f"{self.base_url}{relative_url}", json=data
            )
            return {"error": None, "response": response}
        except Exception as err:
            return {"error": err}


backend = Backend()
