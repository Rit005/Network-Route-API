# 🚀 Network Route Optimization API

A FastAPI-based backend service that simulates a network of interconnected servers and finds the shortest communication route using Dijkstra's Algorithm.

---

## 📌 Features

✅ Add network nodes (servers)

✅ Add network edges (connections with latency)

✅ Find shortest route between two nodes

✅ Calculate total network latency

✅ Store route query history in SQLite

✅ Retrieve route history

✅ List all nodes and edges

✅ Delete nodes and edges

---

## 🛠 Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Dijkstra Algorithm

---

## 📂 Project Structure

```text
network-route-api/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── dijkstra.py
│
├── requirements.txt
├── README.md
└── network.db
```

---

## ⚡ Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd network-route-api
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Mac/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
uvicorn app.main:app --reload
```

Server starts at:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### Nodes

| Method | Endpoint | Description |
|----------|----------|----------|
| POST | `/nodes` | Create node |
| GET | `/nodes` | Get all nodes |
| DELETE | `/nodes/{node_id}` | Delete node |

---

### Edges

| Method | Endpoint | Description |
|----------|----------|----------|
| POST | `/edges` | Create edge |
| GET | `/edges` | Get all edges |
| DELETE | `/edges/{edge_id}` | Delete edge |

---

### Routes

| Method | Endpoint | Description |
|----------|----------|----------|
| POST | `/routes/shortest` | Find shortest route |
| GET | `/routes/history` | Get route history |

---

## 📖 Example

### Add Node

```json
{
  "name": "ServerA"
}
```

Response:

```json
{
  "id": 1,
  "name": "ServerA"
}
```

---

### Add Edge

```json
{
  "source": "ServerA",
  "destination": "ServerC",
  "latency": 5
}
```

Response:

```json
{
  "id": 1,
  "source": "ServerA",
  "destination": "ServerC",
  "latency": 5
}
```

---

### Find Shortest Route

Request:

```json
{
  "source": "ServerA",
  "destination": "ServerD"
}
```

Response:

```json
{
  "total_latency": 10,
  "path": [
    "ServerA",
    "ServerC",
    "ServerD"
  ]
}
```

---

## 🗄 Database Tables

### nodes

| Column |
|----------|
| id |
| name |

### edges

| Column |
|----------|
| id |
| source_id |
| destination_id |
| latency |

### route_history

| Column |
|----------|
| id |
| source |
| destination |
| total_latency |
| path |
| created_at |

---

## 🧠 Algorithm Used

The application uses **Dijkstra's Shortest Path Algorithm** to calculate:

- Minimum latency route
- Optimal path between nodes
- Total route cost

Time Complexity:

```text
O(E log V)
```

where:

- V = number of nodes
- E = number of edges

---

## 👨‍💻 Author

Rithik Sharma
