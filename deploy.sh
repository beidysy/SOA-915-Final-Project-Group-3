#!/bin/bash

echo "🚀 Deploying all microservices to Minikube..."

kubectl apply -f k8s/postgres/
kubectl apply -f k8s/patient-service/
kubectl apply -f k8s/doctor-service/
kubectl apply -f k8s/appointment-service/
kubectl apply -f k8s/notification-service/

echo "✅ All services deployed successfully!"
