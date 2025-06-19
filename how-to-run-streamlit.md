# 🚀 How to Run the Streamlit Frontend (rag-ui)

This guide explains how to build and run the Streamlit-based frontend (`rag-ui`) for the RAG application using Docker.

---

## ✅ Prerequisites

- Docker installed: https://docs.docker.com/get-docker/
- Backend (FastAPI) already running on `http://host.docker.internal:8000/query`
- `.env` file present in the root of the project with required keys (e.g., `OPENAI_API_KEY`)

---

## 📁 Assumed Directory Structure

```
simple-rag/
├── .env
├── streamlit_app/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
```

---

## 🏗 Step 1: Build the Streamlit Docker Image

From the **project root** (`simple-rag/`), run:

```bash
docker build -t rag-ui-image -f streamlit_app/Dockerfile streamlit_app
```

This will create a Docker image with Streamlit and your app code.

---

## 🚀 Step 2: Run the Container

```bash
docker run -d -p 8501:8501 \
  --name rag-ui \
  --env-file .env \
  -e RAG_API_URL=http://host.docker.internal:8000/query \
  rag-ui-image
```

- `--env-file .env`: Loads environment variables (like OpenAI API key, if used by Streamlit).
- `RAG_API_URL`: The endpoint where Streamlit will send requests (served by the FastAPI backend).

---

## 🌐 Step 3: Open the Frontend

Visit in your browser:  
👉 [http://localhost:8501](http://localhost:8501)

---

## 🛑 Cleanup (Optional)

To stop and remove the container:

```bash
docker rm -f rag-ui
```

To remove the image:

```bash
docker rmi rag-ui-image
```

---

## 💡 Tip

If you make changes to `app.py` or `requirements.txt`, rebuild the image before running:

```bash
docker build -t rag-ui-image -f streamlit_app/Dockerfile streamlit_app
```

---

## ✅ That’s it!

Your Streamlit frontend is now running in Docker and communicating with the backend RAG API.
