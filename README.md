# Portainer Service Update Helper.

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

- **0**: Update triggered with success.
- **1**: Missing environment variables
- **2**: Portainer API not reachable (maybe URL is invalid?)
- **3**: Invalid portainer credentials
- **4**: Service not found
- **5**: Update failed
