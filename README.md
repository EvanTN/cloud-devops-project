Cloud DevOps Backend API

![CI Pipeline](https://github.com/EvanTN/cloud-devops-project/actions/workflows/ci.yml/badge.svg)
![Deployed](https://img.shields.io/badge/deployed-Render-blue)


A production-ready backend API built with FastAPI and PostgreSQL, containerized with Docker, continuously tested with GitHub Actions, and deployed to Render.
Designed to serve a separate frontend application deployed on Vercel.

🚀 Tech Stack

FastAPI – Backend framework
PostgreSQL – Relational database
SQLAlchemy + Alembic – ORM & migrations
Docker / Docker Compose – Containerization
GitHub Actions – Continuous Integration
Render – Cloud deployment

✨ Features

RESTful API architecture
Database migrations with Alembic
Dockerized local & production environments
Automated CI pipeline on push & PR
Health check endpoint for monitoring

📌 API Endpoints
Method	Endpoint	Description
GET	/health	Service health check
GET	/items	Retrieve items
POST	/items	Create item

🛠️ Local Development
git clone https://github.com/EvanTN/cloud-devops-project.git
cd cloud-devops-project
docker compose up --build


API runs at:
http://localhost:8000

🔄 CI/CD Pipeline

Runs on every push and pull request
Installs dependencies and runs migrations
Builds Docker image
Blocks deployment if CI fails

☁️ Deployment

The backend is deployed as a containerized web service on Render.

Live API:
👉 https://cloud-devops-api.onrender.com

🎨 Frontend

The frontend is deployed separately using Vercel and consumes this API.
Frontend repository: https://github.com/EvanTN/cloud-devops-project-FrontEnd.git

👤 Author
Evan Nguyen
Computer Science Student @ GMU 2027
