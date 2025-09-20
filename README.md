# ChatMemoryBot (aethermind)

A tiny **chat-with-memory** console app built with **LangChain + OpenAI** that persists:

* **Short‑term memory** in **Redis** (conversation context per session)
* **Long‑term logs** in **SQLite** via **SQLAlchemy** (queryable history)

Use it to prototype an assistant that remembers past turns and lets you print past chats with one command.

---

##  Features

* **Conversation memory** using `ConversationChain` + `ConversationBufferMemory`
* **Redis‑backed chat history** (`RedisChatMessageHistory`) for fast context recall
* **Persistent chat logs** in SQLite (`ChatLog` model) for later analysis
* **One‑command history dump**: type **`/紀錄`** to print all stored Q\&A
* **Simple CLI loop** with graceful exit via **`bye`**

---

##  Architecture

```
+-------------------+        +------------------+
|  Console (CLI)    |  <---> |  Conversation    |
|  while True loop  |        |  Chain (LLM)     |
+-------------------+        +------------------+
           |                               |
           | uses                          | uses
           v                               v
+-------------------+        +---------------------------+
| Redis (short-term)|        | SQLite via SQLAlchemy     |
| RedisChatMessage  |        | ChatLog(user, ai)         |
| History (session) |        | Session() CRUD            |
+-------------------+        +---------------------------+
```

---

##  Project layout

```
ChatMemoryBot/
├─ app.py                # CLI entrypoint (shown below as sample)
├─ chatlog.py            # SQLAlchemy Session & ChatLog model
├─ chatlogs.db           # SQLite database (generated at runtime)
├─ src/aethermind/       # (optional) core library code
├─ tests/                # tests
├─ pyproject.toml        # Poetry project + deps
├─ README.md             # this file
└─ .env                  # OPENAI_API_KEY, REDIS_URL (see below)
```

---

##  Quickstart

### 1) Prerequisites

* Python **3.10 – <4.0**
* **Redis** server running locally (default `redis://localhost:6379`)
* OpenAI API key

### 2) Clone & install (Poetry)

```bash
# clone
git clone <your-repo-url>.git
cd ChatMemoryBot

# install
pip install poetry
poetry install
```

> Not using Poetry? You can `pip install -r <generated requirements>` after exporting, but Poetry is the recommended path.

### 3) Configure environment

Create a **.env** file at the project root:

```env
OPENAI_API_KEY=sk-...
# Optional: override Redis endpoint (default is localhost)
REDIS_URL=redis://localhost:6379
```

### 4) Run

```bash
poetry run python app.py
# or
python app.py
```

You’ll see:

```
你想問 AI 什麼？（輸入 'bye' 結束）：
```

* Type your question → get an answer
* Type **`/紀錄`** → prints all stored Q\&A from SQLite
* Type **`bye`** → exit

---


> **Note**: The snippet above also reads `REDIS_URL` from `.env` for convenience.

---

## ⚙️ Dependencies (from `pyproject.toml`)

* `langchain`
* `langchain-openai`
* `langchain-community`
* `python-dotenv`
* `redis`
* `sqlalchemy`

Managed with **Poetry**. See `pyproject.toml` for exact versions.

---

## 🗄️ Persistence details

* **Redis**: keeps **short‑term** turn‑by‑turn memory for the active `session_id` ("my-session").
* **SQLite** (`chatlogs.db`): appends each Q/A to the `ChatLog` table for long‑term auditing and analytics.

You can rotate `session_id` to separate conversations, or extend `chatlog.py` to include timestamps, user ids, tags, etc.

---


## 🧪 Testing

Place unit tests in `tests/`. Example ideas:

* memory flow (Redis) works end‑to‑end
* DB insert/query for `ChatLog`
* CLI commands: `/紀錄`, `bye`

---

## 🧭 Roadmap

* [ ] Swap `ConversationChain` → `RunnableWithMessageHistory`
* [ ] Add `/search <query>` to query past logs
* [ ] Persist `session_id` per user
* [ ] Dockerfile + `docker-compose` (app + redis)

---


##  Acknowledgments

Built with ❤ using LangChain and OpenAI.
