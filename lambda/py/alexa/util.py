# -*- coding: utf-8 -*-

import requests
from ask_sdk_model import IntentRequest
from typing import Union, Dict, List


def get_restaurants_by_meal(city_data, meal_type):
    """Return a restaurant list based on meal type."""
    # type: (Dict, str) -> List
    return [r for r in city_data["restaurants"] if meal_type in r["meals"]]


def get_restaurants_by_name(city_data, name):
    """Return a restaurant based on name."""
    # type: (Dict, str) -> Dict
    for r in city_data["restaurants"]:
        if r["name"] == name:
            return r
    return {}


def get_attractions_by_distance(city_data, distance):
    """Return a attractions list based on distance."""
    # type: (Dict, str) -> List
    return [a for a in city_data["attractions"]
            if int(a["distance"]) <= int(distance)]


def build_url(city_data, api_info):
    """Return a `request` compatible URL from api properties."""
    # type: (Dict, Dict) -> str
    return "{}:{}{}".format(
        api_info["host"], str(api_info["port"]), api_info["path"].format(
            city=city_data["city"], state=city_data["state"]))


def http_get(url, path_params=None):
    """Return a response JSON for a GET call from `request`."""
    # type: (str, Dict) -> Dict
    response = requests.get(url=url, params=path_params)

    if response.status_code < 200 or response.status_code >= 300:
        response.raise_for_status()
    return response.json()


def get_weather(city_data, api_info):
    """Return weather information for a city by calling API."""
    # type: (Dict, Dict) -> str, str, str
    url = build_url(city_data, api_info)

    response = http_get(url)
    channel = response["query"]["results"]["channel"]

    local_time = channel["lastBuildDate"][17:25]
    current_temp = channel["item"]["condition"]["temp"]
    current_condition = channel["item"]["condition"]["text"]

    return local_time, current_temp, current_condition


def get_resolved_value(request, slot_name):
    """Resolve the slot name from the request."""
    # type: (IntentRequest, str) -> Union[str, None]
    try:
        return request.intent.slots[slot_name].value
    except (AttributeError, ValueError, KeyError, IndexError):
        return None
