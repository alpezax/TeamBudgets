#!/bin/bash

set -e  # Detiene el script ante cualquier error

# Colores
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Instalando pipreqs si no está presente...${NC}"
pip show pipreqs > /dev/null 2>&1 || pip3 install pipreqs --break-system-packages

echo -e "${GREEN}Generando requirements.txt para teambudgets-front...${NC}"
cd teambudgets-front
#pipreqs . --force
cd ..

echo -e "${GREEN}Generando requirements.txt para teambudgets-service...${NC}"
cd teambudgets-service
pipreqs . --force
cd ..

echo -e "${GREEN}Construyendo imágenes Docker...${NC}"

docker build -t alpezax/teambudgets-front:latest ./teambudgets-front
docker build -t alpezax/teambudgets-back:latest ./teambudgets-service

docker push alpezax/teambudgets-front:latest
docker push alpezax/teambudgets-back:latest

echo -e "${GREEN}¡Build completado con éxito!${NC}"

git add -A; git commit -m "Build images"; git push