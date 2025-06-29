# 🚀 TestPilot – AI SaaS Testing & QA Platform

**TestPilot** is an intelligent, end-to-end AI-powered platform that automates test generation, execution, code review, analytics, and secure deployment for modern software projects. It's built for developers, QA engineers, and teams seeking speed, quality, and security in their DevOps workflows.

---

## 🎯 Key Features

### 🔍 AI-Based Test Generation

- Upload code files, API specs (Swagger/OpenAPI), or user stories
- GPT-3.5 turbo auto-generates:
  - ✅ Unit Tests (PyTest/Jest)
  - ✅ API Tests (Newman/Postman)
  - ✅ UI Tests (Playwright/Cypress)
- Auto-tags tests with `@smoke`, `@regression`, `@critical`

---

### 🧪 Test Execution + Automation

- Run tests directly via UI (Streamlit) or CI pipelines
- CLI-compatible with PyTest, Newman, Playwright
- Reports include:
  - ✅ Pass/Fail Summary
  - ✅ Execution Time
  - ✅ Code Coverage
- CI Trigger via GitHub Actions or Jenkins Webhook

---

### 🧠 Code Review + Risk Analyzer (AI-First)

- Analyze uploaded code for:
  - 🛑 Vulnerabilities (via Semgrep/Trivy)
  - 🔎 Code Smells & Bad Patterns
- GPT-4o provides:
  - 🔧 Risk Score (0–100)
  - 💡 Fix Suggestions (LLM-Generated)
  - 🪄 Optional: Auto-refactor insecure code

---

### 📊 Interactive Dashboard

- View testing KPIs and QA insights:
  - Pie Chart: Passed vs Failed
  - Line Graph: Test Runs Over Time
  - Radar: Test Quality Coverage
- Filters: Project, Date, Tag, Coverage %
- LLM Assistant suggests focus areas and predicts failures

---

### 🔐 Auth, Role-Based Access & SaaS

- JWT-based or Firebase Auth login
- Role Permissions:
  - Free Users: 2 test runs/day
  - Pro Users: Unlimited usage
- Multi-tenant schema support (Mongo/Postgres)
- Stripe-ready payments for plan upgrades

---

### ⚙️ GitOps, DevSecOps & Security

- CI/CD Pipelines: GitHub Actions or Jenkins
- Containers: Dockerized backend + frontend
- GitOps: Argo CD deploys to K8s from Helm charts
- Security:
  - ✅ SBOM Generation (Syft)
  - ✅ Vulnerability Scan (Trivy)
  - ✅ Policy Enforcement (OPA/Gatekeeper)
- Bonus: LLM-Based Slack Alerts on:
  - High-risk deployment
  - Failed test summary

---

## 🏗 Architecture Overview

```plaintext
   [Frontend UI: Streamlit]
            ↓
   [Backend API: FastAPI]
        ↙       ↘
 [OpenAI LLM]   [Test Runner (Pytest, Newman)]
        ↓
     MongoDB / PostgreSQL
        ↓
     GitHub / Jenkins
        ↓
  [K8s Cluster (ArgoCD + Helm)]
```

---

## 📦 Tech Stack

| Layer          | Technology                                |
| -------------- | ----------------------------------------- |
| UI             | Streamlit                                 |
| Backend        | FastAPI                                   |
| AI Integration | OpenAI GPT-4o + LangChain                 |
| Test Runners   | PyTest, Newman, Playwright                |
| Auth           | Firebase Auth / JWT                       |
| CI/CD          | GitHub Actions / Jenkins + Docker         |
| GitOps         | Argo CD + Helm                            |
| Security       | Trivy, Semgrep, OPA/Gatekeeper            |
| Database       | MongoDB / PostgreSQL (Multi-Tenant Ready) |

---

## 🚀 Quick Start (Local Development)

### 1. Clone the Repo

```bash
git clone https://github.com/your-org/testpilot
cd testpilot
```

### 2. Start Backend

```bash
cd backend
uvicorn main:app --reload
```

### 3. Start Frontend

```bash
cd frontend
streamlit run app.py
```

### 4. Test via Curl

```bash
curl -X POST http://localhost:8000/gen-tests \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a, b): return a + b", "type": "unit"}'
```

---

## 🐳 Docker + Kubernetes

### Docker

```bash
docker build -t testpilot-backend ./backend
docker build -t testpilot-frontend ./frontend
```

### Kubernetes (Helm + Argo CD)

1. Helm Chart: `k8s/helm/testpilot`

```yaml
# Chart.yaml
name: testpilot
version: 0.1.0
```

```yaml
# values.yaml
backend:
  image: <your-registry>/testpilot-backend
  port: 8000

frontend:
  image: <your-registry>/testpilot-frontend
  port: 8501
```

2. Argo CD App:

```yaml
# deploy/testpilot-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: testpilot
spec:
  source:
    repoURL: https://github.com/your-org/testpilot
    path: k8s/helm/testpilot
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: testpilot
  syncPolicy:
    automated:
      selfHeal: true
```

---

## 🔐 Gatekeeper Policy Example

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          missing := {label | input.review.object.metadata.labels[label] == ""}
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }
```

---

## 💬 LLM Slack Alerts (Optional)

```python
from openai import OpenAI
from slack_sdk import WebClient

def analyze_failure(log: str):
    response = OpenAI().chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Analyze this CI log:\n{log}"}]
    )
    return response.choices[0].message.content

def send_to_slack(channel, msg):
    client = WebClient(token="xoxb-xxxx")
    client.chat_postMessage(channel=channel, text=msg)
```

---

## 📂 Project Structure

```
testpilot/
├── backend/
│   ├── routers/
│   │   ├── test_gen.py
│   │   ├── run_tests.py
│   │   ├── code_reviews.py
│   │   └── dashboard.py
│   └── main.py
├── frontend/
│   ├── app.py
│   └── pages/
│       ├── generate.py
│       ├── run.py
│       ├── review.py
│       └── dashboard.py
├── k8s/
│   └── helm/
│       └── testpilot/
│           ├── Chart.yaml
│           └── values.yaml
├── deploy/
│   └── testpilot-app.yaml
└── README.md
```

---

## 🙌 Contribute & Collaborate

- Pull Requests are welcome
- Raise issues for features or bugs
- Looking to integrate HuggingFace, Claude, or local LLMs next? Let’s collaborate.

---

## 📄 License

MIT © 2025 TestPilot Contributors

---

## 👥 Maintainer

**Saksham Goyal**
[🔗 LinkedIn](https://www.linkedin.com/in/saksham-goyal-ab3a1817b/) | [🐙 GitHub](https://github.com/sakshamgoyal01)

---
