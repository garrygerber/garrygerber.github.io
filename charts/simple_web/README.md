# Simple Web Application Helm Chart

This Helm chart deploys a simple web application on Kubernetes.

## Prerequisites

- Kubernetes 1.16+
- Helm 3.0+
- KEDA installed
- Ingress Controller installed

## Installing the Chart

To install the chart with the release name `simple-web`:

```bash
$ helm install simple-web .
```

## Uninstalling the Chart

To uninstall/delete the `simple-web` deployment:

```bash
$ helm delete simple-web
```
