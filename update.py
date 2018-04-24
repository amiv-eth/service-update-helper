#!/usr/bin/env python3
"""Portainer Service Update Helper.

[Portainer](portainer.readthedocs.io) is a useful tool to manage docker swarm
clusters, but the API to update services requires quite a lot of steps.

This script handles everything needed to trigget a forced update of a service,
(which also causes nodes to pull new images, e.g. newer 'latest' images) and
can be configured with environment variables:

- `CI_DEPLOY_URL`: The URL of the
  [Portainer API](http://portainer.readthedocs.io/en/stable/API.html)
- `CI_DEPLOY_USERNAME`: portainer username
- `CI_DEPLOY_PASSWORD`: portainer user password
- `CI_DEPLOY_SERVICE`: name of the service to update
- `CI_DEPLOY_ENDPOINT`: (optional) portainer endpoint number, uses 1
                        (primary endpoint) by default

Exit Codes:

0: Update triggered with success.
1: Missing environment variables
2: Portainer API not reachable (maybe URL is invalid?)
3: Invalid portainer credentials
4: Service not found
5: Update failed
"""

from sys import exit
from os import getenv
import requests


# Use the primary endpoint by default
DEFAULT_ENDPOINT = 1


def main():
    """Update a service using the portainer API."""
    session = requests.Session()

    # 0. Get configuration from environment
    # -------------------------------------

    url = getenv('CI_DEPLOY_URL')
    username = getenv('CI_DEPLOY_USERNAME')
    password = getenv('CI_DEPLOY_PASSWORD')
    endpoint = getenv('CI_DEPLOY_ENDPOINT', DEFAULT_ENDPOINT)
    service = getenv('CI_DEPLOY_SERVICE')

    error = False
    if not url:
        print("Please specify the portainer API url with the environment "
              "variable 'CI_DEPLOY_URL'!")
        error = True
    else:
        url = url[:-1] if url.endswith('/') else url
    if not (username and password):
        print("Please specify valid username and password for portainer with "
              "'CI_DEPLOY_USERNAME' and 'CI_DEPLOY_PASSWORD' environment "
              "variables!")
        error = True
    if not service:
        print("Please specify the service name with the environment variable "
              "'CI_DEPLOY_SERVICE!")
        error = True
    if error:
        exit(1)

    # 1. Get token
    # ------------

    print("Requesting portainer token...")
    login_data = {"username": username, "password": password}
    try:
        response = session.post('%s/auth' % url, json=login_data)
        if response.status_code == 404:
            raise RuntimeError
    except (requests.exceptions.RequestException, RuntimeError):
        print('The Portainer URL is invalid!')
        exit(2)

    if response.status_code == 422:
        print("The Portainer credentials are invalid!")
        exit(3)

    session.headers['Authorization'] = 'Bearer %s' % response.json()['jwt']

    # 2. Get service id, specs and version
    # ------------------------------------

    service_url = '%s/endpoints/%s/docker/services/%s' % (url, endpoint,
                                                          service)

    print("Fetching service information...")
    service_data = session.get(service_url)

    if service_data.status_code == 404:
        print("The service '%s' could not be found!" % service)
        exit(4)
    else:
        service_data = service_data.json()

    version = service_data['Version']['Index']
    spec = service_data['Spec']

    print("Service '%s' found with version number: %s" % (service, version))

    # 3. Force service update
    # -----------------------

    # The complete spec must be sent, partial fields do not work
    # Increment the 'ForceUpdate' field to trigger a forced update
    spec['TaskTemplate']['ForceUpdate'] += 1

    print('Triggering forced service update...')
    update = session.post('%s/update?version=%s' % (service_url, version),
                          json=spec)

    if update.status_code != 200:
        print('The update failed with the following message:')
        print("'%s'" % update.json()['message'])
        exit(5)

    print('Success!')


if __name__ == '__main__':
    main()
