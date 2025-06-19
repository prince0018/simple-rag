# 🛠️ How to Run the Project Locally

This guide will help you run the complete Retrieval-Augmented Generation (RAG) system including:

- ✅ FastAPI-based RAG backend
- ✅ Prometheus monitoring
- ✅ Grafana dashboard
- ✅ (Optional) Streamlit frontend UI

---

## 🧠 Prerequisites

- Docker Desktop installed → [Download Here](https://www.docker.com/products/docker-desktop)
- Clone the repository:

```bash
git clone https://github.com/prince0018/simple-rag.git
cd simple-rag
```

---

## ✅ 1. Create `.env` File

```bash
touch .env
```

Add your credentials:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_PROJECT_ID=your_project_id   # optional
```

---

## ✅ 2. Build the RAG Backend

```bash
docker build -t simple-rag-api .
```

---

## ✅ 3. Run the FastAPI Backend

```bash
docker run -d -p 8000:8000 \
  --env-file .env \
  --name rag-app \
  simple-rag-api
```

- Swagger UI: http://localhost:8000/docs
- Metrics: http://localhost:8000/metrics

---

## ✅ 4. Run Prometheus

```bash
docker run -d -p 9090:9090 \
  -v $(pwd)/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
  --name prometheus \
  prom/prometheus
```

- UI: http://localhost:9090

---

## ✅ 5. Run Grafana

```bash
docker run -d -p 3000:3000 \
  --name grafana \
  grafana/grafana
```

- Grafana: http://localhost:3000
- Login: `admin / admin` (change password after login)

### Connect to Prometheus:

1. Settings > Data Sources > Add Data Source
2. Select **Prometheus**
3. URL: `http://host.docker.internal:9090` (Windows/Mac)
4. Click **Save & Test**

---

## ✅ 6. (Optional) Run Streamlit Frontend

If `streamlit_app/app.py` exists:

```bash
docker run -d -p 8501:8501 \
  --name rag-ui \
  -v $(pwd)/streamlit_app:/app \
  -e RAG_API_URL=http://host.docker.internal:8000/query \
  python:3.11-slim \
  streamlit run /app/app.py --server.port 8501 --server.address 0.0.0.0
```

- Streamlit: http://localhost:8501

---

## 🔄 Cleanup

```bash
docker stop rag-app prometheus grafana rag-ui
docker rm rag-app prometheus grafana rag-ui
```

---

## 🧾 Summary Table

| Component     | Port | URL                             |
|---------------|------|----------------------------------|
| FastAPI       | 8000 | http://localhost:8000/docs       |
| Prometheus    | 9090 | http://localhost:9090            |
| Grafana       | 3000 | http://localhost:3000            |
| Streamlit UI  | 8501 | http://localhost:8501 (optional) |