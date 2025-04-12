SOA-915 Final Project – Group 3
Hospital Appointment System
A containerized, microservices-based Hospital Appointment System built with Flask and PostgreSQL. Deployed on Kubernetes (Minikube) with integrated monitoring and logging using Prometheus, Grafana, and Loki.

Table of Contents
Overview

Architecture

Tech Stack

Features

Getting Started

Microservice Structure

Deployment

Monitoring & Logging

Overview
This system allows patients to book appointments with doctors. When appointments are created, updated, or deleted, notifications are generated. The services communicate through RESTful APIs and run in a Kubernetes cluster using Minikube for local deployment.

Architecture
Microservices: Patient, Doctor, Appointment, Notification

Independent PostgreSQL databases per service

RESTful communication

JWT-based access control

Kubernetes for orchestration

Monitoring: Prometheus + Grafana

Logging: Loki + Promtail

Tech Stack
Component	Tool / Framework
Language	Python 3.12
Framework	Flask
Database	PostgreSQL
Containerization	Docker
Orchestration	Kubernetes (Minikube)
CI/CD	GitHub Actions
Monitoring	Prometheus, Grafana
Logging	Loki, Promtail
Testing	pytest
Features
CRUD APIs for all entities

Notification service with appointment-based triggers

Patient-specific notification filtering (via X-Patient-ID header)

JWT-based API access control

Centralized logging (Loki)

Horizontal Pod Autoscaling (HPA)

CI/CD with GitHub Actions

Getting Started
Prerequisites
Python 3.12

Docker

Minikube

Helm

kubectl

Clone the Repository
bash
Copy
Edit
git clone https://github.com/beidysy/SOA-915-Final-Project-Group-3.git
cd SOA-915-Final-Project-Group-3
Microservice Structure
Each service contains:

bash
Copy
Edit
├── app.py            # Flask app entry point
├── models.py         # SQLAlchemy models
├── routes.py         # REST API endpoints
├── Dockerfile        # Docker image build
├── requirements.txt  # Dependencies
├── config.py         # Environment configuration
Deployment
1. Start Minikube
bash
Copy
Edit
minikube start --cpus=4 --memory=8192
eval $(minikube docker-env)
2. Build Docker Images
bash
Copy
Edit
docker build -t patient-service:latest ./patient-service
docker build -t doctor-service:latest ./doctor-service
docker build -t appointment-service:latest ./appointment-service
docker build -t notification-service:latest ./notification-service
3. Load Images into Minikube
bash
Copy
Edit
minikube image load patient-service:latest
minikube image load doctor-service:latest
minikube image load appointment-service:latest
minikube image load doctor-service:latest
4. Deploy Services to Kubernetes
bash
Copy
Edit
kubectl apply -f k8s/postgres/
kubectl apply -f k8s/patient-service/
kubectl apply -f k8s/doctor-service/
kubectl apply -f k8s/appointment-service/
kubectl apply -f k8s/notification-service/
Monitoring & Logging
Deploy Monitoring (Prometheus + Grafana)
bash
Copy
Edit
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
Deploy Logging (Loki + Promtail)
bash
Copy
Edit
kubectl create namespace logging
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack -n logging --set grafana.enabled=true --set promtail.enabled=true
Access Grafana Dashboard
bash
Copy
Edit
kubectl port-forward svc/loki-grafana -n logging 3000:80
Then open your browser at http://localhost:3000 and log in:

Username: admin

Password: prom-operator

Example Loki Query:

scss
Copy
Edit
rate({container="appointment-service"}[1m])
CI/CD with GitHub Actions
Every push to the main branch triggers:

Linting and unit tests with pytest

Docker image builds

Deployment via deploy.sh

The workflow is defined in .github/workflows/main.yml.
