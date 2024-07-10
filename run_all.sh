#!/bin/bash

# Paso 1: Configuro el Docker Compose
echo "Levantando Docker Compose..."
docker-compose up -d

# Espero unos segundos para asegurarse de que el contenedor de la base de datos esté listo
echo "Esperando a que el contenedor de la base de datos esté listo..."
sleep 60

# Paso 2: Iniciar la base de datos
echo "Inicializando la base de datos..."
docker exec -i postgres_db psql -U fsantoliquido -d airlines -f /scripts/create_tables.sql

# Paso 3: Popular la base de datos
echo "Popopular la base de datos..."
docker build -t populate -f Dockerfile.populate .
docker run --rm --network itba-cde-cloud-architecture_default populate

# Paso 4: Ejecutar consultas
echo "Construyendo y realizando las consultas..."
docker build -t consultas -f Dockerfile.consultas .
docker run --rm --network itba-cde-cloud-architecture_default consultas

echo "Proceso completado"