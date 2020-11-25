# HELM Chart for docker-hub-rate-limit-exporter

This repository enables prometheus scrapping of dockerhub rate limits by providing a ready to use docker image and helm chart. It is based on the work done by gitlab as described in their blogpost: https://about.gitlab.com/blog/2020/11/18/docker-hub-rate-limit-monitoring/

## How to install the chart

You can install the chart by downloading this repository and running the helm install command. Follow the steps below:

1. run `git clone https://github.com/viadee/docker-hub-rate-limit-exporter.git`
2. run `helm install <release name> docker-hub-rate-limit-exporter/chart --namespace=<desired namespace>`

By running the above command you will install the docker-hub-rate-limit-exporter into your cluster. It will expose the dockerhub limits in the prometheus format.

## How to configure your docker credentials

If your kubernetes cluster does not authenticate with dockerhub you don't need to do anything here. However, if it does, you need to configure the crendetials with helm values. This is because the docker-hub-rate-limit-exporter does not use the dockerhub account assosiated with the docker context of your kubernetes-cluster. You can configure it to do so by following the steps below:

1. Create a helm value file as per the example in this repository (see: helm-values.example.yaml)
2. Fill in the variables `dockerhubUsername` and `dockerhubPassword`. It is recommended to use a dockerhub access token for the password.
3. run `helm install <release name> docker-hub-rate-limit-exporter/helm --namespace=<desired namespace> -f <name of value file>`

## How to tell prometheus to scrap the metrics

We recommend you to use the prometheus kubernetes operator to run prometheus in your cluster (see: https://github.com/prometheus-operator/prometheus-operator). If you run the operator you can create a `ServiceMonitor` resource to tell prometheus how to scrap the docker-hub-rate-limit-exporter. See the example below:

```
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
    name: docker-hub-rate-limit-exporter
    labels:
        app: docker-hub-rate-limit-exporter
        # you may need to add further labels here depending on your prometheus configuration
spec:
    selector:
        matchLabels:
            app.kubernetes.io/name: docker-hub-rate-limit-exporter
    endpoints:
        - port: http
          path: "/"
          interval: 10s
    jobLabel: docker-hub-rate-limit-exporter
    namespaceSelector: ### this part can be ommited if your ServiceMonitor resource lives in the same namespace as the docker-hub-rate-limit-exporter sercice
        matchNames:
            - <the namespace where the docker-hub-rate-limit-exporter lives>
```
