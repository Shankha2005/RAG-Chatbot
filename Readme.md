# 🤖 RAG Chatbot

A full-stack **Retrieval-Augmented Generation (RAG)** application that lets users upload PDF documents and interact with them through an AI-powered chat interface.

The application uses **FastAPI** for the backend, **React + Vite** for the frontend, **ChromaDB** for vector storage, and **Google Gemini 2.5 Flash** for generating context-aware responses.

---

## ✨ Features

- 📄 **PDF Upload & Processing** — Extract and split document content into meaningful chunks.
- 🔍 **Semantic Search** — Retrieve relevant information using ChromaDB vector search.
- 🧠 **RAG Pipeline** — Combines retrieved document context with Gemini 2.5 Flash.
- ⚡ **Streaming Responses** — AI responses are streamed in real time.
- 📚 **Source Citations** — Tracks document and page information for references.
- 💻 **Modern UI** — Responsive React interface built with Vite.
- 🏗️ **Modular Architecture** — Separate frontend, backend, database, and service layers.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React, Vite, JavaScript, CSS |
| **Backend** | FastAPI, Python |
| **AI / RAG** | Gemini 2.5 Flash, LangChain |
| **Vector Database** | ChromaDB |
| **Document Processing** | PDF parsing & text chunking |

---

## 🔄 How It Works

```text
PDF Upload
    ↓
Text Extraction & Chunking
    ↓
Generate Embeddings
    ↓
Store in ChromaDB
    ↓
User Question
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
Gemini 2.5 Flash
    ↓
Streaming Response
```

---

## 📂 Project Structure

```text
RAG-CHATBOT/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Configuration
│   │   ├── db/           # ChromaDB setup
│   │   ├── services/     # RAG & document processing
│   │   └── main.py       # FastAPI entry point
│   ├── chroma_data/      # Local vector database
│   ├── .env              # Environment variables
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## 🚀 Run Locally

### Backend

```bash
cd backend

python -m venv venv
```

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `backend/.env`:

```env
GEMINI_API_KEY="your-gemini-api-key"
CHUNK_SIZE=512
CHUNK_OVERLAP=64
```

Start the server:

```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

Backend API: `http://localhost:8000`

API Docs: `http://localhost:8000/docs`

---

## 🔐 Security

- API keys are stored in environment variables.
- `.env`, `venv`, `node_modules`, and generated ChromaDB data are excluded using `.gitignore`.

---

## 📌 Future Improvements

- User authentication
- Conversation history
- Multiple document collections
- Support for more file formats
- Hybrid search & re-ranking
- Docker-based deployment

---

## 📄 License

MIT License