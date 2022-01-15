from urllib.parse import urlencode

import requests
from django.conf import settings
from requests import exceptions, status_codes
from requests.exceptions import RequestException
from rest_framework import status

centrifugo = "58c2400b-831d-411d-8fe8-31b6e337738b"
PLUGIN_ID = "616991e5ef1c19335a2869f4"
ORG_ID = "619ba4671a5f54782939d384"


class DataStorage:
    def __init__(self, request=None):
        self.read_api = (
            "https://api.zuri.chat/data/read/{pgn_id}/{collec_name}/{org_id}?{query}"
        )
        # self.upload_test_api = "http://127.0.0.1:8000/api/v1/testapi/{pgn_id}"
        self.write_api = "https://api.zuri.chat/data/write"
        self.delete_api = "https://api.zuri.chat/data/delete"

        if request is None:
            self.plugin_id = PLUGIN_ID
            self.organization_id = ORG_ID
        else:
            self.plugin_id = request.META.get("PLUGIN_ID", PLUGIN_ID)
            self.organization_id = request.META.get("ORG_ID")

    def write(self, collection_name, data):
        body = dict(
            plugin_id=self.plugin_id,
            organization_id=self.organization_id,
            collection_name=collection_name,
            payload=data,
        )
        try:
            response = requests.post(url=self.write_api, json=body)
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        if response.status_code == 201:
            return response.json()
        return {"status_code": response.status_code, "message": response.reason}

    def update(self, collection_name, document_id, data):
        body = dict(
            plugin_id=self.plugin_id,
            organization_id=self.organization_id,
            collection_name=collection_name,
            object_id=document_id,
            payload=data,
        )
        try:
            response = requests.put(url=self.write_api, json=body)
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        if response.status_code == 200:
            return response.json()
        return {"status_code": response.status_code, "message": response.reason}

    def read(self, collection_name, filter={}):
        try:
            query = urlencode(filter)
        except Exception as e:
            print(e)
            return None

        url = self.read_api.format(
            pgn_id=self.plugin_id,
            org_id=self.organization_id,
            collec_name=collection_name,
            query=query,
        )

        try:
            response = requests.get(url=url)
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        if response.status_code == 200:
            return response.json().get("data")
        return {"status_code": response.status_code, "message": response.reason}

    def delete(self, collection_name, document_id):
        body = dict(
            plugin_id=self.plugin_id,
            organization_id=self.organization_id,
            collection_name=collection_name,
            object_id=document_id,
        )
        try:
            response = requests.post(url=self.delete_api, json=body)
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        if response.status_code == 200:
            return response.json()
        return {"status_code": response.status_code, "message": response.reason}


DB = DataStorage()


def centrifugo_publish(room, event, data, plugin_url="music.zuri.chat"):
    data_to_publish = {
        "status": 200,
        "event": event,
        "plugin_url": plugin_url,
        "plugin_id": settings.PLUGIN_ID,
        "data": data,
    }

    headers = {
        "Content-type": "application/json",
        "Authorization": "apikey " + centrifugo,
    }
    url = "https://realtime.zuri.chat/api"
    command = {
        "method": "publish",
        "params": {"channel": room, "data": data_to_publish},
    }
    try:
        response = requests.post(url=url, headers=headers, json=command)
    except requests.RequestException as error:
        raise RequestException(error)

    return {"status_code": response.status_code, "message": response.json()}


def get_org_members(org_id=None):
    if org_id is not None:
        url = f"https://api.zuri.chat/organizations/{org_id}/members"
        try:
            response = requests.get(url=url)
            if response.status_code == status.HTTP_200_OK:
                return response.json()
            return {"error": "Error in getting the org members"}
        except exceptions.RequestException as e:
            return {"status": status.HTTP_400_BAD_REQUEST, "error": e}
    return {"message": "invalid org id"}
    