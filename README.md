# SOA-915-Final-Project-Group-3
# Hospital Appointment System

This is a microservices-based hospital appointment system built with Flask and PostgreSQL, deployed on Kubernetes with monitoring and logging integrated via Prometheus, Grafana, and Loki.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Getting Started](#getting-started)
- [Microservices](#microservices)
- [Deployment](#deployment)
- [Monitoring & Logging](#monitoring--logging)

## Overview

The system allows patients to book appointments with doctors. Notifications are generated and stored based on appointment actions. The services communicate via REST APIs and are deployed to a local Kubernetes cluster using Minikube.

## Architecture

- Microservices: Patient, Doctor, Appointment, Notification
- Independent PostgreSQL databases per service
- RESTful communication between services
- JWT-based authentication for API access
- Kubernetes used for container orchestration
- Monitoring via Prometheus and Grafana
- Logging via Loki and Promtail

## Tech Stack

- Python 3.12
- Flask
- PostgreSQL
- Docker
- Kubernetes (Minikube)
- Helm
- Prometheus + Grafana
- Loki + Promtail
- pytest (for testing)

## Features

- CRUD operations for Patients, Doctors, Appointments
- Notification service for appointment updates
- Patient-specific notification retrieval
- Input validation and error handling
- Token-based authentication with JWT
- Real-time monitoring and centralized logging

## Getting Started

### Prerequisites

- Python 3.12
- Docker
- Minikube
- Helm
- kubectl

### Clone the repository

```bash
git clone https://github.com/beidysy/SOA-915-Final-Project-Group-3/

Start Minikube
minikube start --cpus=4 --memory=8192

Build Docker Images
eval $(minikube docker-env)

# Build each service
cd patient-service && docker build -t patient-service:latest .
cd ../doctor-service && docker build -t doctor-service:latest .
cd ../appointment-service && docker build -t appointment-service:latest .
cd ../notification-service && docker build -t notification-service:latest .

Build Docker Images
eval $(minikube docker-env)

# Build each service
cd patient-service && docker build -t patient-service:latest .
cd ../doctor-service && docker build -t doctor-service:latest .
cd ../appointment-service && docker build -t appointment-service:latest .
cd ../notification-service && docker build -t notification-service:latest .


Load Images into Minikube
minikube image load patient-service:latest
minikube image load doctor-service:latest
minikube image load appointment-service:latest
minikube image load notification-service:latest

Deploy Services to Kubernetes
kubectl apply -f k8s/postgres/
kubectl apply -f k8s/patient-service/
kubectl apply -f k8s/doctor-service/
kubectl apply -f k8s/appointment-service/
kubectl apply -f k8s/notification-service/

Microservices
Each microservice follows the same structure:

app.py: Main entry point

models.py: SQLAlchemy models

routes.py: API endpoints

Dockerfile: Container setup

requirements.txt: Python dependencies

config.py: Configuration using environment variables

Monitoring & Logging
Deploy Monitoring Stack
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring


Deploy Logging Stack (Loki)
kubectl create namespace logging
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack -n logging --set grafana.enabled=true --set promtail.enabled=true


Access Grafana Dashboard
kubectl port-forward svc/loki-grafana -n logging 3000:80

Open http://localhost:3000 and log in with:
Username: admin
Password: prom-operator




rate({container="appointment-service"}[1m])

