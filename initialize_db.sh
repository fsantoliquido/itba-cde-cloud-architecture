#!/bin/bash

# Nombre del contenedor
CONTAINER_NAME=postgres_db

# Nombre de la base de datos, usuario y archivo SQL
DB_NAME=airlines
DB_USER=fsantoliquido
SQL_FILE=/scripts/create_tables.sql

# Ejecutar el script SQL dentro del contenedor
docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -f $SQL_FILE