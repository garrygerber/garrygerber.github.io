{{/*
Expand the name of the chart.
*/}}
{{- define "simple-web.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "simple-web.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" $name .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create a suffix with chart version and image tag
*/}}
{{- define "simple-web.versionSuffix" -}}
{{- $tag := default .Chart.AppVersion .Values.image.tag -}}
{{- printf "%s-%s" .Chart.Version $tag | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a name with version suffix
*/}}
{{- define "simple-web.versionedName" -}}
{{- $name := include "simple-web.fullname" . -}}
{{- $version := include "simple-web.versionSuffix" . | replace "." "-" -}}
{{- printf "%s-%s" $name $version | lower | trunc 63 | trimSuffix "-" -}}
{{- end }}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "simple-web.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "simple-web.labels" -}}
helm.sh/chart: {{ include "simple-web.chart" . }}
{{ include "simple-web.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "simple-web.selectorLabels" -}}
app.kubernetes.io/name: {{ include "simple-web.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/tag: {{ default .Chart.AppVersion .Values.image.tag }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "simple-web.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "simple-web.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}