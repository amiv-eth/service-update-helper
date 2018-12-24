# Cluster Service Update Helper

This script handles everything needed to trigger a forced update of a service,
(which also causes nodes to pull new images, e.g. newer 'latest' images) and
can be configured with environment variables:

- `CI_DEPLOY_URL`: The URL of the [Service-Update-Helper-Service](https://gitlab.ethz.ch/amiv/service-update-helper-service)
- `CI_DEPLOY_TOKEN`: authorization token
- `CI_DEPLOY_SERVICE`: name of the service to update

Exit Codes:

- **0**: Update triggered with success.
- **1**: Missing environment variables
- **2**: Service-Update-Helper-Service is not reachable (maybe URL is invalid?)
- **3**: Invalid authorization token
- **4**: No permission to update the given service
- **5**: Service not found
- **6**: Update failed
