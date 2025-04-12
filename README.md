# SOA-915 Final Project – Group 3  
## Hospital Appointment System

A containerized, microservices-based Hospital Appointment System built with Flask and PostgreSQL. Deployed on Kubernetes (Minikube) with integrated monitoring and logging using Prometheus, Grafana, and Loki.

---

## 📚 Table of Contents

- [Overview](#overview)  
- [Architecture](#architecture)  
- [Tech Stack](#tech-stack)  
- [Features](#features)  
- [Getting Started](#getting-started)  
- [Microservice Structure](#microservice-structure)  
- [Deployment](#deployment)  
- [Monitoring & Logging](#monitoring--logging)  
- [CI/CD](#cicd)

---

## Overview

This system allows patients to book appointments with doctors. When appointments are created, updated, or deleted, notifications are generated. The services communicate through RESTful APIs and run in a Kubernetes cluster using Minikube for local deployment.

---

## Architecture

- Microservices: Patient, Doctor, Appointment, Notification  
- Independent PostgreSQL databases per service  
- RESTful communication  
- JWT-based access control  
- Kubernetes for orchestration  
- Monitoring: Prometheus + Grafana  
- Logging: Loki + Promtail  

---

## Tech Stack

| Component        | Tool / Framework           |
|------------------|----------------------------|
| Language         | Python 3.12                |
| Framework        | Flask                      |
| Database         | PostgreSQL                 |
| Containerization | Docker                     |
| Orchestration    | Kubernetes (Minikube)      |
| CI/CD            | GitHub Actions             |
| Monitoring       | Prometheus, Grafana        |
| Logging          | Loki, Promtail             |
| Testing          | pytest                     |

---

## Features

- CRUD APIs for all entities  
- Notification service with appointment-based triggers  
- Patient-specific notification filtering (via `X-Patient-ID`)  
- JWT-based API access control  
- Centralized logging (Loki)  
- Horizontal Pod Autoscaling (HPA)  
- CI/CD with GitHub Actions  

---

## Getting Started

### Prerequisites

- Python 3.12  
- Docker  
- Minikube  
- Helm  
- kubectl  

### Clone the Repository

```bash
git clone https://github.com/beidysy/SOA-915-Final-Project-Group-3.git
cd SOA-915-Final-Project-Group-3
