import os
import json

import pytest


poke_api = os.environ.get('URL_POKE_API')


mock_data_berries = {
  "count": 5,
  "next": None,
  "previous": None,
  "results": [
    {
      "name": "cheri",
      "url": f"{poke_api}berry/1"
    },
    {
      "name": "chesto",
      "url": f"{poke_api}berry/2"
    },
    {
      "name": "pecha",
      "url": f"{poke_api}berry/3"
    },
    {
      "name": "rawst",
      "url": f"{poke_api}berry/4"
    },
    {
      "name": "aspear",
      "url": f"{poke_api}berry/5"
    },
  ]
}

mock_data_berry = {
    "firmness": {
    "name": "soft",
    "url": "https://pokeapi.co/api/v2/berry-firmness/2/"
    },
    "flavors": [
    {
      "flavor": {
        "name": "spicy",
        "url": "https://pokeapi.co/api/v2/berry-flavor/1/"
      },
      "potency": 10
    },
    ],
    "growth_time": 3,
    "id": 1,
    "item": {
    "name": "cheri-berry",
    "url": "https://pokeapi.co/api/v2/item/126/"
    },
    "max_harvest": 5,
    "name": "cheri",
    "natural_gift_power": 60,
}


# Mock  to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0].split("/")[-1] == 'berry':
        return MockResponse(mock_data_berries, 200)
    elif args[0].split("/")[-1].isdigit():
        return MockResponse(mock_data_berry, 200)

    return MockResponse(None, 404)


def test_gapi(mocker, client):
    # Patch 'requests.get'
    mocker.patch("requests.get", side_effect=mocked_requests_get)


    response = client.get("allBerryStats")
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data['berries_names'] == ['cheri', 'chesto', 'pecha', 'rawst', 'aspear']
    assert response_data['min_growth_time'] == 3
    assert response_data['max_growth_time'] == 3

