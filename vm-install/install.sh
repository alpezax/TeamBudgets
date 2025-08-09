#!/bin/bash
# --------------------------------------
# Script para instalar Docker y Docker Compose
# en una VM Ubuntu/Debian (como e2-micro en GCP)
# --------------------------------------
set -e
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
docker --version

