# 🚀 How to Run the Full RAG Application (Backend + Frontend)

This guide walks you through the full setup for running both the FastAPI backend and Streamlit frontend using Docker.

---

## ✅ Prerequisites

- Docker installed: https://docs.docker.com/get-docker/
- `.env` file with your OpenAI key (or clone from repo if already included)

---

## 📁 Project Structure

```
simple-rag/
├── .env
├── Dockerfile             # ⬅️ Backend (FastAPI)
├── main.py                # ⬅️ Backend entry point
├── requirements.txt       # ⬅️ Backend dependencies
└── streamlit_app/
    ├── Dockerfile         # ⬅️ Frontend (Streamlit)
    ├── app.py
    └── requirements.txt
```

---

## 🧾 Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/simple-rag.git
cd simple-rag
```

Make sure you have a `.env` file in the root directory with your OpenAI API key:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🛠 Step 2: Build and Run the Backend (FastAPI)

### 🔨 Build Backend Image

```bash
docker build -t rag-api-image .
```

### 🚀 Run Backend Container

```bash
docker run -d -p 8000:8000 \
  --name rag-api \
  --env-file .env \
  rag-api-image
```

🔗 Check if backend is running: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🎨 Step 3: Build and Run the Frontend (Streamlit)

### 🔨 Build Frontend Image

```bash
docker build -t rag-ui-image -f streamlit_app/Dockerfile streamlit_app
```

### 🚀 Run Frontend Container

```bash
docker run -d -p 8501:8501 \
  --name rag-ui \
  --env-file .env \
  -e RAG_API_URL=http://host.docker.internal:8000/query \
  rag-ui-image
```

🔗 Open in browser: [http://localhost:8501](http://localhost:8501)

---

## 🛑 Cleanup Commands

### Remove containers

```bash
docker rm -f rag-api rag-ui
```

### Remove images

```bash
docker rmi -f rag-api-image rag-ui-image
```

---

## ✅ You're All Set!

You now have both backend and frontend running with Docker. Happy building!
