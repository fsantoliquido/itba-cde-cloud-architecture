# Nombre del contenedor de PostgreSQL
CONTAINER_NAME="postgres_db"

# Archivo SQL con las instrucciones de creación de tablas
SQL_FILE=create_tables.sql

# Verifica si el contenedor está corriendo
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "El contenedor $CONTAINER_NAME está corriendo. Ejecutando el script SQL..."
    docker exec -i $CONTAINER_NAME psql -U "fsantoliquido" -d "airlinesflights" < $SQL_FILE
    echo "Script SQL ejecutado exitosamente."
else
    echo "El contenedor $CONTAINER_NAME no está corriendo. Por favor, inícialo y vuelve a intentarlo."
fi