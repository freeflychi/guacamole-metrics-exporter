# Copyright (c) 2022 Cisco Systems, Inc. and its affiliates
# All rights reserved.

# The license notice is:
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Based on information from https://github.com/ridvanaltun/guacamole-rest-api-documentation

import config
import metricslogger
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prometheus_client import start_http_server, Summary, Gauge


# suppress insecure warning if env var set
if config.suppress_ssl_warning == 'y' or config.suppress_ssl_warning == 'Y':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    metricslogger.logger.warning("SSL verification warning suppressed")


# Prometheus CollectorRegistry
USERS = Gauge('number_of_users', 'Number of Users in DB')
CONNECTIONS = Gauge('number_of_connections', 'Number of connections in DB')
ACTIVE_CONNECTIONS = Gauge(
    'number_of_active_connections', 'Number of active connections')


class metrics:
    api = "/guacamole/api/session/data/mysql/"
    token = ""

    def getToken(self):
        try:
            url = f"https://{config.guacamole_host}/guacamole/api/tokens"

            payload = f'username={config.guacamole_user}&password={config.guacamole_pass}'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.request(
                "POST", url, headers=headers, data=payload, verify=False)

            # extract auth token
            j_token = response.json()
            self.token = j_token['authToken']

        except(Exception) as error:
            metricslogger.logger.error(f"failed to get token - {error}")

    def numUsers(self):
        try:
            url = f"https://{config.guacamole_host}{self.api}users?token={self.token}"
            payload = {}
            headers = {}

            response = requests.request(
                "GET", url, headers=headers, data=payload, verify=False)

            j_users = response.json()
            num_users = len(j_users)
            metricslogger.logger.info(f"number of users={num_users}")

            # prometheus exporter
            USERS.set(num_users)

        except(Exception) as error:
            metricslogger.logger.error(
                f"failed to get number of users - {error}")

    def numConnections(self):
        try:
            url = f"https://{config.guacamole_host}{self.api}connections?token={self.token}"

            response = requests.request("GET", url, verify=False)

            j_con = response.json()
            num_connections = len(j_con)
            metricslogger.logger.info(
                f"number of connections={num_connections}")

            # prometheus exporter
            CONNECTIONS.set(num_connections)

        except(Exception) as error:
            metricslogger.logger.error(
                f"failed to get number of connections - {error}")

    def numActiveConnections(self):
        try:
            url = f"https://{config.guacamole_host}{self.api}activeConnections?token={self.token}"
            response = requests.request("GET", url, verify=False)

            j_active_con = response.json()
            num_active_connections = len(j_active_con)
            metricslogger.logger.info(
                f"active connections={num_active_connections}")

            # prometheus exporter
            ACTIVE_CONNECTIONS.set(num_active_connections)

        except(Exception) as error:
            metricslogger.logger.error(
                f"failed to get active connections - {error}")


def main():
    getMetrics = metrics()

    # start prometheus web server
    start_http_server(8000)

    while True:
        getMetrics.getToken()
        getMetrics.numUsers()
        getMetrics.numConnections()
        getMetrics.numActiveConnections()
        time.sleep(10)


if __name__ == '__main__':
    main()
