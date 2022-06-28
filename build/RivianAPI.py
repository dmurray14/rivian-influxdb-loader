import time
from datetime import datetime, timedelta
import argparse
import requests
from dataclasses import dataclass
import os


LOGIN_URL = "https://auth.rivianservices.com/auth/api/v1/token/auth"
REFRESH_URL = "https://auth.rivianservices.com/auth/api/v1/token/refresh"
GQL_ORDERS_URL = "https://rivian.com/api/gql/orders/graphql/"
GQL_T2D_URL = "https://rivian.com/api/gql/t2d/graphql/"
CONTENT_TYPE = 'application/json;charset=UTF-8'
CLIENT_ID = "rivian.mobile.sc12bjxe8lmhkul"
CLIENT_SECRET = "rlL058p5kipkZr0C85KrdA4AZ0QBNVh75zXWwEWf"
DC_CID = "account--9dfce4c4-dbd1-4e70-8735-12e9c776afbf--c202d410-ed84-48b5-8c5b-4b91d1a14648"

VEHICLE_URL = "https://cesium.rivianservices.com"


class RivianAPI:
    def __init__(self, vehicleId, username, password) -> None:
        self._access_token  = ''
        self._refresh_token = ''
        self._token_expires_ts = 0

        self._username = username
        self._password = password

        self._session = requests.Session()

        self.authenticate()

        self._vehicle_data = {} #self.get_vehicle_all()

    def authenticate(self) -> None:
        headers = {'Content-Type': CONTENT_TYPE}
        payload = {
            "username": self._username,
            "pwd": self._password,
            "source": "mobile",
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }

        response = self._session.post(url=LOGIN_URL, headers=headers, json=payload)
        result = response.json()

        self._access_token = result['access_token']
        self._refresh_token = result['refresh_token']
        self._token_expires_ts = datetime.now() + timedelta(seconds=result['expires_in'])

    def refresh_token(self) -> None:
        headers = {'Content-Type': CONTENT_TYPE}
        payload = {
            "token": self._refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }

        response = self._session.post(url=REFRESH_URL, headers=headers, json=payload)
        result = response.json()
        print(result)

        self._access_token = result['access_token']
        self._token_expires_ts = datetime.now() + timedelta(seconds=result['expires_in'])



    def api_query(self, endpoint, payload) -> dict:
        if self._token_expires_ts < datetime.now():
            self.refresh_token()

        headers = {
            'Content-Type': CONTENT_TYPE,
            'dc-cid': DC_CID,
            'Authorization': 'Bearer ' + self._access_token
        }
        try:
            response = self._session.post(url=VEHICLE_URL + endpoint, headers=headers, data=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            return {}
        except:
            print("Unknown error")
            return {}
        return response.json()

    def get_vehicle_all(self) -> dict:
        payload = f'''
        {{
            "car": "{VEHICLE_ID}",
            "properties": [
                "$gnss",
                "adas/*",
                "body/*",
                "core/*",
                "dynamics/*",
                "energy_storage/*",
                "telematics/*",
                "thermal/*",
                "vas/*"
            ]
        }}'''

        result = self.api_query('/v2/vehicle/latest', payload)
        return result


    def get_new_data(self):
        new_data = self.get_vehicle_all()
        old_data = self._vehicle_data

        if new_data == {}:
            #No data, or error
            return

        new_data_elements = []

        for tag in new_data['data']:
            data_is_new = True #default to true so the first run populates the db

            ts_new = new_data["data"][tag][0]
            dt_new = datetime.strptime(ts_new, '%Y-%m-%dT%H:%M:%S.%fZ')


            if old_data != {} and tag in old_data['data']:
                ts_old = old_data["data"][tag][0]
                dt_old = datetime.strptime(ts_old, '%Y-%m-%dT%H:%M:%S.%fZ')
                if dt_new <= dt_old:
                    data_is_new = False

            if data_is_new:
                dtype = type(new_data["data"][tag][1])

                if dtype in (float, int, str):
                    new_data_elements.append(
                        {
                        "measurement": "rivian",
                        "tags": {"sensor": tag},
                        "fields": {
                                dtype.__name__: new_data["data"][tag][1],
                                },
                        "time": dt_new.isoformat(),
                        }
                    )

        return new_data_elements
