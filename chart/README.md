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

| Parameter                         | Description                                                                                                       | Default |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------- |
| `config.exporterPort`             | Port the deployment exposes                                                                                       | `80`    |
| `config.exporterVerbosity`        | Loglevel of the deployment                                                                                        | `1`     |
| `config.dockerhubUsername`        | To authenticate with dockerhub                                                                                    | `nil`   |
| `config.dockerhubPassword`        | To authenticate with dockerhub (use access token)                                                                 | `nil`   |
| `serviceMonitor.enabled`          | If true, creates a ServiceMonitor instance                                                                        | `false` |
| `serviceMonitor.additionalLabels` | Configure additional labels for the servicemonitor                                                                | `{}`    |
| `serviceMonitor.namespace`        | The namespace into which the servicemonitor is deployed. If not set, will the same as the namespace of this chart | `nil`   |
| `serviceMonitor.interval`         | The interval with which prometheus will scrape                                                                    | `30s`   |
| `serviceMonitor.scrapeTimeout`    | The timeout for the scrape request                                                                                | `10s`   |
