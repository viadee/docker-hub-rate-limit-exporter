# docker-hub-rate-limit-exporter Helm Chart

## How to install the chart

You can install the chart by downloading this repository and running the helm install command. Follow the steps below:

1. run `git clone https://github.com/viadee/docker-hub-rate-limit-exporter.git`
2. run `helm install <release name> docker-hub-rate-limit-exporter/chart --namespace=<desired namespace>`

By running the above command you will install the docker-hub-rate-limit-exporter into your cluster. It will expose the dockerhub limits in the prometheus format.

## Uninstalling the Chart

To uninstall/delete the my-release deployment:

```console
helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration

| Parameter           | Description                                       | Default |
| ------------------- | ------------------------------------------------- | ------- |
| `exporterPort`      | Port the deployment exposes                       | `80`    |
| `exporterVerbosity` | Loglevel of the deployment                        | `1`     |
| `dockerhubUsername` | To authenticate with dockerhub                    | `nil`   |
| `dockerhubPassword` | To authenticate with dockerhub (use access token) | `nil`   |
