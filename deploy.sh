#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🔧 Building Docker images..."

# Build Docker images for each microservice
docker build -t patient-service:latest ./patient-service
docker build -t doctor-service:latest ./doctor-service
docker build -t appointment-service:latest ./appointment-service
docker build -t notification-service:latest ./notification-service

echo "📦 Images built successfully."

# Enable Minikube Docker environment
echo "🛠️ Switching to Minikube Docker environment..."
eval $(minikube docker-env)

# Apply Kubernetes manifests
echo "🚀 Applying Kubernetes manifests..."

kubectl apply -f k8s/postgres
kubectl apply -f k8s/patient-service
kubectl apply -f k8s/doctor-service
kubectl apply -f k8s/appointment-service
kubectl apply -f k8s/notification-service

echo "✅ Deployment complete. All services are deployed to Minikube."
