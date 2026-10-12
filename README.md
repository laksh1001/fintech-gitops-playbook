```markdown
# 🚀 Fintech GitOps & Full-Stack Observability Pipeline

A production-grade, end-to-end Kubernetes delivery and observability platform built for a polyglot fintech microservices architecture. This repository implements GitOps continuous deployment using **Argo CD**, real-time metric monitoring with **Prometheus & Grafana**, and centralized log aggregation via the **Elastic Stack (ECK) & Filebeat**.

---

## 🏗️ System Architecture

```text
                               ┌─────────────────────────┐
                               │  GitHub Repository      │
                               │  fintech-gitops-playbook│
                               └────────────┬────────────┘
                                            │
                                            │ Continuous Reconciliation
                                            ▼
                               ┌─────────────────────────┐
                               │       Argo CD           │
                               │  (namespace: argocd)    │
                               └────────────┬────────────┘
                                            │
                      ┌─────────────────────┼─────────────────────┐
                      │                     │                     │
                      ▼                     ▼                     ▼
             ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
             │  auth-service   │   │  ledger-service │   │  notification   │
             │   (Go / 8080)   │   │(Python/FastAPI) │   │  service (Go)   │
             └────────┬────────┘   └────────┬────────┘   └────────┬────────┘
                      │                     │                     │
                      └─────────────────────┼─────────────────────┘
                                            │
                                namespace: fintech
                                            │
               ┌────────────────────────────┴────────────────────────────┐
               │                                                         │
               ▼                                                         ▼
  ┌─────────────────────────┐                               ┌─────────────────────────┐
  │  Metrics & Monitoring   │                               │  Log Aggregation        │
  │  (namespace: monitoring)│                               │  (namespace: logging)   │
  ├─────────────────────────┤                               ├─────────────────────────┤
  │  • Prometheus           │                               │  • Filebeat (DaemonSet) │
  │  • Grafana (Port 3000)  │                               │  • Elasticsearch (9200) │
  │  • kube-state-metrics   │                               │  • Kibana (Port 5601)   │
  └─────────────────────────┘                               └─────────────────────────┘

```

---

## 📑 Table of Contents

* [Architecture & Tech Stack](https://www.google.com/search?q=%23-architecture--tech-stack)
* [Microservices Overview](https://www.google.com/search?q=%23-microservices-overview)
* [Prerequisites](https://www.google.com/search?q=%23-prerequisites)
* [Quick Start & Deployment Guide](https://www.google.com/search?q=%23-quick-start--deployment-guide)
* [1. Cluster & Namespace Preparation](https://www.google.com/search?q=%231-cluster--namespace-preparation)
* [2. Deploy Microservices via Argo CD](https://www.google.com/search?q=%232-deploy-microservices-via-argo-cd)
* [3. Deploy Prometheus & Grafana Monitoring](https://www.google.com/search?q=%233-deploy-prometheus--grafana-monitoring)
* [4. Deploy Elastic Stack & Filebeat Logging](https://www.google.com/search?q=%234-deploy-elastic-stack--filebeat-logging)


* [Verification & Access Matrix](https://www.google.com/search?q=%23-verification--access-matrix)
* [Production Engineering & Troubleshooting](https://www.google.com/search?q=%23-production-engineering--troubleshooting)
* [Repository Structure](https://www.google.com/search?q=%23-repository-structure)

---

## 🛠️ Tech Stack

| Category | Tools & Technologies |
| --- | --- |
| **Container Orchestration** | Kubernetes (k8s / Minikube / k3s) |
| **GitOps Continuous Delivery** | Argo CD, Helm v3, Kustomize |
| **Microservices Stack** | Go, Python (FastAPI), Docker |
| **Metrics & Dashboarding** | Prometheus, Grafana, kube-state-metrics |
| **Log Aggregation & Analytics** | Elastic Stack (ECK), Elasticsearch, Filebeat, Kibana |
| **Configuration & Scripting** | Bash, YAML, Helm Values |

---

## 🧩 Microservices Overview

All microservices run inside the `fintech` namespace and expose `/healthz` endpoints for liveness/readiness probes:

1. **`auth-service`** (Go): Handles authentication and token validation. Listens on port `8080`.
2. **`ledger-service`** (Python / FastAPI): Manages transaction logs, accounting ledgers, and balance queries. Listens on port `8081` (includes OpenAPI `/docs`).
3. **`notification-service`** (Go): Processes transactional alerts and email/SMS triggers. Listens on port `8082`.

---

## ⚙️ Prerequisites

Before starting deployment, ensure you have the following installed:

* **Kubernetes Cluster** v1.24+
* **kubectl** CLI
* **Helm** v3.x
* **Git** CLI

---

## 🚀 Quick Start & Deployment Guide

### 1. Cluster & Namespace Preparation

Create the dedicated namespaces required for isolation:

```bash
kubectl create namespace fintech
kubectl create namespace argocd
kubectl create namespace monitoring
kubectl create namespace logging

```

---

### 2. Deploy Microservices via Argo CD

Install Argo CD into the `argocd` namespace and apply the application manifests:

```bash
# Install Argo CD
kubectl apply -n argocd -f [https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml](https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml)

# Access Argo CD Server
kubectl port-forward svc/argocd-server -n argocd 8080:443

```

Apply the GitOps ApplicationSet manifest:

```bash
kubectl apply -f argocd/fintech-app.yaml --server-side

```

---

### 3. Deploy Prometheus & Grafana Monitoring

Add the Prometheus Helm repository and install the kube-prometheus-stack:

```bash
helm repo add prometheus-community [https://prometheus-community.github.io/helm-charts](https://prometheus-community.github.io/helm-charts)
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --set grafana.service.type=ClusterIP

```

Port-forward Grafana to access dashboards:

```bash
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring

```

* **Grafana URL**: `http://localhost:3000`
* **Default Login**: Username: `admin` | Password: `prom-operator`

---

### 4. Deploy Elastic Stack & Filebeat Logging

Add the Elastic Helm repository:

```bash
helm repo add elastic [https://helm.elastic.co](https://helm.elastic.co)
helm repo update

```

Create the `filebeat-values.yaml` file to stream container logs to Elasticsearch:

```yaml
filebeatConfig:
  filebeat.yml: |
    filebeat.inputs:
    - type: container
      paths:
        - /var/log/containers/*.log
      processors:
      - add_kubernetes_metadata:
          host: ${NODE_NAME}
          in_cluster: true

    output.elasticsearch:
      hosts: ['https://elasticsearch-master:9200']
      username: 'elastic'
      password: 'cVsG71idegsnmzHR'
      ssl.verification_mode: none

```

Deploy Filebeat via Helm:

```bash
helm install filebeat elastic/filebeat -n logging -f filebeat-values.yaml

```

Port-forward Kibana:

```bash
kubectl port-forward svc/kibana-kibana 5601:5601 -n logging

```

---

## 🔍 Verification & Access Matrix

### Local Verification Endpoints

| Component | Target URL | Expected Output / View |
| --- | --- | --- |
| **Auth Service** | `http://localhost:8080/healthz` | `{"status":"HEALTHY","service":"auth-service"}` |
| **Ledger Service** | `http://localhost:8081/healthz` | `{"status":"HEALTHY","service":"ledger-service"}` |
| **Ledger Swagger UI** | `http://localhost:8081/docs` | OpenAPI Interactive Documentation |
| **Notification Service** | `http://localhost:8082/healthz` | `{"status":"HEALTHY","service":"notification-service"}` |
| **Argo CD UI** | `http://localhost:8080` | All Applications `Synced` & `Healthy` |
| **Grafana** | `http://localhost:3000` | Cluster CPU/Memory Working Set Gauges |
| **Kibana Discover** | `http://localhost:5601` | Filter: `kubernetes.namespace : "fintech"` |

### Kibana Data View Setup

1. Open Kibana (`http://localhost:5601`).
2. Go to **Management** > **Data Views** > **Create Data View**.
3. Name: `filebeat-*` | Index Pattern: `filebeat-*` | Timestamp: `@timestamp`.
4. Open **Analytics** > **Discover** and run the search query:
```kql
kubernetes.namespace : "fintech"

```



---

## 🛠️ Production Engineering & Troubleshooting

### Issue 1: Git Bash Process Substitution Error (`/proc/fd/63`)

* **Symptom**: Helm installation fails with `failed parsing --set-file data: open /proc/1686/fd/63` on Windows Git Bash when using inline command substitution `<(...)`.
* **Root Cause**: Windows environment lacks native `/proc/fd/` FIFO pipes.
* **Fix**: Write configurations directly into a physical `filebeat-values.yaml` file instead of passing process substitution strings directly in the terminal command line.

### Issue 2: Argo CD ApplicationSet CRD Metadata Overhead

* **Symptom**: Argo CD reconciliation failed due to `metadata.annotations: Too long: must have at most 262144 bytes`.
* **Root Cause**: `kubectl apply` client-side apply stores previous state in `kubectl.kubernetes.io/last-applied-configuration`, exceeding annotation size limits for complex CRDs.
* **Fix**: Enforce Server-Side Apply to delegate state management to the Kubernetes API server:
```bash
kubectl apply -f argocd/fintech-app.yaml --server-side

```



---

## 📁 Repository Structure

```text
.
├── argocd/                  # Argo CD Application & ApplicationSet manifests
│   └── fintech-app.yaml
├── helm/                    # Helm charts for fintech microservices
│   └── fintech-app/
├── k8s/                     # Kubernetes base manifests & Kustomize overlays
│   └── base/
├── services/                # Source code for microservices
│   ├── auth-service/        # Go authentication microservice
│   ├── ledger-service/      # Python/FastAPI accounting service
│   └── notification-service/# Go notification dispatch service
├── filebeat-values.yaml     # Custom Filebeat configuration for ECK log ingestion
└── README.md                # Project documentation

```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

```

```
