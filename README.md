# 🚀 microservices-k8s-deployment

Lightweight demo of a simple microservices stack (**frontend + backend + MongoDB**) with Kubernetes manifests for local testing.

---

## 📂 Contents
- `frontend/` — Flask frontend that calls backend and renders a simple dashboard (`templates/index.html`).
- `backend/` — Flask backend that reads/writes simple values to MongoDB.
- `k8s/` — Kubernetes manifests for deploying the stack (`backend.yaml`, `frontend.yaml`, `mongo.yaml`, `mongo-express.yaml`).

---

## 🎯 Goals
- Small demo showing how to run a frontend and backend with MongoDB.
- Example Kubernetes manifests for local clusters (minikube, kind) or a small cloud cluster.

---

## 🖼️ Architecture Diagram
![System architecture diagram](screenshots/architecture-diagram.png)

> Figure: High-level system architecture — frontend calls backend; backend stores data in MongoDB; `mongo-express` provides a DB UI.

---

## ⚙️ Requirements
- Python 3.8+ to run the services locally
- Docker (for container images) or a Kubernetes cluster (minikube/kind/managed)
- `kubectl` configured for your cluster

---

## 💻 Quick Local (no Kubernetes) — Recommended for Development

Start **MongoDB** (use 4.4 for older CPUs without AVX):

```bash
# recommended for older hardware or local dev
docker run -d --name mongo -p 27017:27017 mongo:4.4
```

Start **mongo-express** (UI):

```bash
docker run -d --name mongo-express --link mongo:mongo -p 8081:8081 \
  -e ME_CONFIG_MONGODB_SERVER=mongo \
  -e ME_CONFIG_MONGODB_PORT=27017 \
  -e ME_CONFIG_BASICAUTH=false \
  mongo-express
```

Run **backend** (from repo root):

```bash
cd backend
pip install -r requirements.txt
export PORT=8000
export MONGO_HOST=mongo
export MONGO_PORT=27017
python app.py
```

Run **frontend**:

```bash
cd frontend
pip install -r requirements.txt
export PORT=9000
export BACKEND_URL=http://localhost:8000
python app.py
# open http://localhost:9000
```

📌 Notes:
- The backend currently exposes a simple `GET /api/add/<name>` and `/api/get` used by the frontend.
- The frontend template includes an in-page UI to add names and show env variables.

---

## 🐳 Running with Docker Images

Build images and run containers (example):

```bash
docker build -t prajwalmalokar/backend:latest ./backend
docker build -t prajwalmalokar/frontend:latest ./frontend
# run with appropriate envs and links or a user-defined network
```

---

## ☸️ Kubernetes Deployment

Apply the manifests in `k8s/`:

```bash
kubectl apply -f k8s/mongo.yaml
kubectl apply -f k8s/mongo-express.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
```

Accessing services:
- `mongo-express` Service in `k8s/mongo-express.yaml` is configured to forward to container port **8081**.
  - Check services: `kubectl get svc`
  - Use `kubectl port-forward` or a LoadBalancer/NodePort depending on your cluster.
- `backend` Service maps port **80 → 8000**.
- `frontend` Service maps port **80 → 9000**.
- Use `kubectl port-forward svc/frontend 9000:80` to access frontend.

---

## ⚠️ Important Notes
- MongoDB **5.0+ requires CPUs with AVX support**. If your node does not have AVX the official `mongo:5` image may fail to start. Use `mongo:4.4` for dev/local.
- `ME_CONFIG_MONGODB_SERVER` should be the Mongo host (service name or FQDN). Do **not** append ports here — use `ME_CONFIG_MONGODB_PORT` or full connection string.
- Avoid committing **secrets** (DB passwords, private keys, kubeconfig) to this repo. Use Kubernetes Secrets or external secret managers.

---

## 📜 License
This repository contains example code for **demo purposes**. No license file included — add one if you plan to publish.

