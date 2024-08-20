# Simple Web Application Helm Chart

This Helm chart deploys a simple web application on Kubernetes with advanced configuration options.

## Features

- Configurable deployment with customizable resources
- Ingress support for external access
- KEDA integration for auto-scaling
- Network policies for enhanced security
- Pod Disruption Budget for high availability
- Helm tests for deployment validation
- Configurable probes and security contexts

## Prerequisites

- Kubernetes 1.16+
- Helm 3.0+
- KEDA installed (optional, required for auto-scaling)
- Ingress Controller installed (optional, required for Ingress resource)

## Installing the Chart

To install the chart with the release name `simple-web`:

```bash
$ helm repo add simple-web https://garrygerber.github.io/simple-web
$ helm repo update
$ helm install simple-web simple-web/simple-web
```

## Uninstalling the Chart

To uninstall/delete the `simple-web` deployment:

```bash
$ helm uninstall simple-web
```

## Configuration

The following table lists all the configurable parameters of the simple-web chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `enabled` | Enable or disable the entire chart | `true` |
| `replicaCount` | Number of replicas for the deployment | `3` |
| `image.registry` | Container image registry | `acrinterview.azurecr.io` |
| `image.repository` | Container image repository | `simple-web` |
| `image.tag` | Container image tag | `latest` |
| `image.pullPolicy` | Container image pull policy | `IfNotPresent` |
| `nameOverride` | Override the name of the chart | `""` |
| `fullnameOverride` | Override the full name of the release | `""` |
| `service.enabled` | Enable or disable the Kubernetes Service | `true` |
| `service.type` | Kubernetes Service type | `ClusterIP` |
| `service.ports` | List of ports for the service | See below |
| `container.resources.limits.cpu` | CPU limit for the container | `100m` |
| `container.resources.limits.memory` | Memory limit for the container | `128Mi` |
| `container.resources.requests.cpu` | CPU request for the container | `50m` |
| `container.resources.requests.memory` | Memory request for the container | `64Mi` |
| `container.ports` | List of ports for the container | See below |
| `serviceAccount.create` | Create a service account | `true` |
| `serviceAccount.annotations` | Annotations for the service account | `{}` |
| `serviceAccount.name` | Name of the service account | `""` |
| `podSecurityContext` | Security context for the pod | `{}` |
| `containerSecurityContext` | Security context for the container | `{}` |
| `imagePullSecrets` | Image pull secrets for private registries | `{}` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class name | `""` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.tls` | Ingress TLS configuration | `{}` |
| `ingress.hosts` | Ingress hostnames and paths | See below |
| `networkPolicy.enabled` | Enable network policy | `false` |
| `networkPolicy.policyTypes` | Network policy types | `["Ingress", "Egress"]` |
| `networkPolicy.ingress` | Ingress network policy rules | See below |
| `networkPolicy.egress` | Egress network policy rules | See below |
| `nodeSelector` | Node selector for pod assignment | `{}` |
| `tolerations` | Tolerations for pod assignment | `[]` |
| `affinity` | Affinity rules for pod assignment | `{}` |
| `priorityClassName` | Priority class name for the pod | `""` |
| `podAnnotations` | Annotations for the pod | `{}` |
| `livenessProbe` | Liveness probe configuration | See below |
| `readinessProbe` | Readiness probe configuration | See below |
| `kedaScaler.enabled` | Enable KEDA auto-scaling | `true` |
| `kedaScaler.minReplicaCount` | Minimum number of replicas for KEDA | `1` |
| `kedaScaler.maxReplicaCount` | Maximum number of replicas for KEDA | `10` |
| `kedaScaler.triggers` | KEDA scaling triggers | See below |
| `podDisruptionBudget.enabled` | Enable Pod Disruption Budget | `false` |
| `podDisruptionBudget.maxUnavailable` | Maximum number of unavailable pods | `1` |