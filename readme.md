# Simple RAG API

Retrieval‑Augmented‑Generation micro‑service built with **LangChain + OpenAI**, served by **FastAPI**, packaged in **Docker**, delivered via **GitHub Actions**, and monitored with **Prometheus + Grafana**.

---

## 1 – Architecture at a Glance

```
User ─▶ FastAPI (/query) ─▶ LangChain
                       │        │
                       │        └─▶ OpenAI LLM
                       └─▶ FAISS Vector DB

FastAPI ─▶ /metrics ─▶ Prometheus ─▶ Grafana Dashboard
```

| Layer            | Tool                                    | Purpose                                 |
| ---------------- | --------------------------------------- | --------------------------------------- |
| Vector DB        | **FAISS**                               | Local, lightning‑fast similarity search |
| Embeddings / LLM | **OpenAI** (`ada‑002`, `gpt‑3.5‑turbo`) | Create embeddings & generate answers    |
| Orchestration    | **LangChain**                           | 3‑line `ConversationalRetrievalChain`   |
| Web API          | **FastAPI**                             | Swagger docs, async, `/query` endpoint  |
| Packaging        | **Docker**                              | Reproducible container                  |
| CI/CD            | **GitHub Actions → Docker Hub**         | Auto‑build & push on every `git push`   |
| Metrics          | **prometheus\_fastapi\_instrumentator** | One‑liner exposes `/metrics`            |
| Collector        | **Prometheus**                          | Time‑series DB & PromQL                 |
| Dashboards       | **Grafana**                             | Live graphs + alert rules               |

---

## 2 – Quick Start

```bash
# ① Ingest docs → FAISS
python rag.py --add docs/alex.txt

# ② Build + run API
docker build -t simple-rag-api .
docker run -d -p 8000:8000 --env-file .env --name rag-app simple-rag-api
#  http://localhost:8000/docs   (Swagger)
#  http://localhost:8000/metrics (Prometheus)

# ③ Spin‑up monitoring stack
#   Prometheus
docker run -d -p 9090:9090 \
  -v $PWD/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
  --name prometheus prom/prometheus
#   Grafana
docker run -d -p 3000:3000 --name grafana grafana/grafana
#  Login admin/admin → add Prometheus @ http://host.docker.internal:9090
```

---

## 3 – File Layout

```
simple-rag/
├─ app/                 # FastAPI router + LangChain setup
├─ faiss_index/         # Vector store on disk
├─ docs/                # Source text files
├─ monitoring/
│   └─ prometheus.yml   # Prometheus scrape config
├─ rag.py               # CLI: ingest + chat
├─ main.py              # FastAPI entrypoint
├─ Dockerfile
├─ requirements.txt
└─ .github/workflows/
    └─ docker-build.yml # CI/CD pipeline
```

---

## 4 – CI/CD Pipeline

1. Push to **master** → GitHub Actions fires.
2. Build Docker image.
3. Login to Docker Hub (secrets `DOCKER_USERNAME`, `DOCKER_PASSWORD`).
4. Push `prince0018/simple-rag-api:latest`.

---

## 5 – Core Prometheus Queries

| Panel                | Query (PromQL)                                                                          |
| -------------------- | --------------------------------------------------------------------------------------- |
| **QPS**              | `rate(http_requests_total[1m])`                                                         |
| **p95 Latency**      | `histogram_quantile(0.95, sum by (le)(rate(http_request_duration_seconds_bucket[5m])))` |
| **Memory Usage**     | `process_resident_memory_bytes`                                                         |
| **Error Rate (5xx)** | `rate(http_requests_total{status=~"5.."}[5m])`                                          |

---

## 6 – Deploy to EC2 in 3 Commands

```bash
ssh -i key.pem ec2-user@<IP>
docker pull prince0018/simple-rag-api:latest
echo OPENAI_API_KEY=sk-xxx > .env
docker run -d -p 80:8000 --env-file .env simple-rag-api
```

---

## 7 – Next Ideas

- JWT / OAuth auth layer
- Streaming responses over WebSocket
- Autoscale with Kubernetes + HPA
- AlertManager → Slack / e‑mail
- Front‑end chat (React / Next.js)

> **Result:** A portable, auto‑built, real‑time‑observable RAG micro‑service. Clone, run two Docker commands, start asking questions 🚀

