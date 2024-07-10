
# Análisis de la Base de Datos de Vuelos

## Descripción del Dataset

La base de datos de vuelos incluye información detallada sobre vuelos, reservas, boletos y pasajeros. A continuación se presenta una breve descripción de las tablas principales:

- **bookings**: Contiene información sobre las reservas realizadas.
- **tickets**: Almacena información sobre los boletos emitidos a los pasajeros.
- **ticket_flights**: Relaciona los boletos con los segmentos de vuelo.
- **flights**: Incluye detalles sobre los vuelos, como puntos de partida y destino, fechas de salida y llegada.
- **airports**: Proporciona información sobre los aeropuertos.
- **boarding_passes**: Contiene información sobre los pases de abordar emitidos a los pasajeros.
- **seats**: Información sobre los asientos disponibles en las aeronaves.
- **aircrafts**: Detalles sobre los modelos de aeronaves y su configuración de cabina.

## Preguntas de Negocio

### 1. Frecuencia de Rutas
**Pregunta**: ¿Cuáles son las rutas más frecuentemente voladas en los últimos tres meses?

**Consulta SQL**:
```sql
SELECT f.departure_airport, f.arrival_airport, COUNT(*) AS flight_count
FROM flights f
WHERE f.scheduled_departure >= NOW() - INTERVAL '3 months'
GROUP BY f.departure_airport, f.arrival_airport
ORDER BY flight_count DESC;
```

**Explicación**: Esta consulta identifica las rutas más populares en los últimos tres meses al contar la frecuencia de vuelos entre cada par de aeropuertos de salida y llegada.

### 2. Puntualidad de Vuelos
**Pregunta**: ¿Cuál es la tasa de puntualidad de los vuelos (llegadas a tiempo versus retrasos) en los últimos tres meses?

**Consulta SQL**:
```sql
SELECT COUNT(CASE WHEN actual_arrival <= scheduled_arrival THEN 1 END) * 100.0 / COUNT(*) AS on_time_percentage,
       COUNT(CASE WHEN actual_arrival > scheduled_arrival THEN 1 END) * 100.0 / COUNT(*) AS delayed_percentage
FROM flights
WHERE scheduled_departure >= NOW() - INTERVAL '3 months';
```

**Explicación**: Esta consulta calcula la tasa de puntualidad de los vuelos, diferenciando entre vuelos que llegaron a tiempo y aquellos que se retrasaron en los últimos tres meses.

### 3. Origen y Destino Más Populares
**Pregunta**: ¿Cuáles son los aeropuertos de origen y destino más populares en los últimos tres meses?

**Consulta SQL**:
```sql
SELECT departure_airport, arrival_airport, COUNT(*) AS flight_count
FROM flights
WHERE scheduled_departure >= NOW() - INTERVAL '3 months'
GROUP BY departure_airport, arrival_airport
ORDER BY flight_count DESC;
```

**Explicación**: Esta consulta identifica los aeropuertos de origen y destino más populares contando la cantidad de vuelos entre cada par de aeropuertos en los últimos tres meses.

### 4. Tarifas Promedio
**Pregunta**: ¿Cuál ha sido la tarifa promedio por vuelo y por clase en los últimos tres meses?

**Consulta SQL**:
```sql
SELECT f.flight_id, tf.fare_conditions, AVG(tf.amount) AS avg_fare
FROM ticket_flights tf
JOIN flights f ON tf.flight_id = f.flight_id
WHERE f.scheduled_departure >= NOW() - INTERVAL '3 months'
GROUP BY f.flight_id, tf.fare_conditions
ORDER BY f.flight_id, tf.fare_conditions;
```

**Explicación**: Esta consulta calcula la tarifa promedio por vuelo y por clase de viaje en los últimos tres meses, proporcionando información valiosa para evaluar el rendimiento financiero.



# Explicación del desarrollo de los ejercicios 3 a 5:

Para simpleza de los ejercicios, si bien no es una buena práctica, creo la base y dejo las credenciales hardcodeadas.

## Ejercicio 3: Creo la Base de Datos 

En este ejercicio, creo la base de  datos en PostgreSQL usando Docker. Para eso se genera un archvio yml donde creamos el container postgres_db que usa el archivo create_tables.sql para general los esquemas.

### Pasos:

1. **Configurar Docker Compose**:

   ```yaml
   version: '3.8'

   services:
     db:
       build: .
       container_name: postgres_db
       environment:
         POSTGRES_USER: fsantoliquido
         POSTGRES_PASSWORD: itba1234
         POSTGRES_DB: airlines
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data
         - ./create_tables.sql:/scripts/create_tables.sql
   volumes:
     postgres_data:
   ```

2. **Levantar Docker Compose (corriendo desde la terminal)**:

   ```sh
   docker-compose up -d
   ```

3. **Inicializar la Base de Datos (con el archivo bash)**:

   Ejecutar el script `initialize_db.sh`:

   ```sh
   #!/bin/bash

   # Nombre del contenedor
   CONTAINER_NAME=postgres_db

   # Nombre de la base de datos, usuario y archivo SQL
   DB_NAME=airlines
   DB_USER=fsantoliquido
   SQL_FILE=create_tables.sql

   # Ejecutar el script SQL dentro del contenedor
   docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -f /scripts/$SQL_FILE
   ```

## Ejercicio 4: Popular la Base de Datos

Acá populamos la base con los datos necesarios. Lo hacemos por batches de 100 para evitar problemas de memoria. Previo a esto se creó un archivo con los inserts de sql que necesitamos para el ejercicio llamado "transformed_inserts.sql". Como es un archivo pesado, no fue pusheado a GitHub. Sin embargo, dejo un archivo llamado "transformed_isnerts_sample.sql" con el mismo formato pero menos rows. 

### Pasos:

1. **Crear el Dockerfile para el contenedor de populate**:

   ```Dockerfile
   FROM python:3.8-slim

   # Instalar psycopg2
   RUN pip install psycopg2-binary

   # Crear directorio de trabajo
   WORKDIR /scripts

   # Copiar el script de Python y el archivo SQL al contenedor
   COPY populate_db.py /scripts/
   COPY transformed_inserts.sql /scripts/

   # Ejecutar el script de Python
   CMD ["python", "/scripts/populate_db.py"]
   ```

2. **Construir y ejecutar el contenedor `populate`**:

   ```sh
   docker build -t populate -f Dockerfile.populate .
   docker run --rm --network itba-cde-cloud-architecture_default populate
   ```

## Ejercicio 5: Consultas a la Base de Datos

Realizamos cinco consultas SQL que agregan valor al negocio. Primero las testeamos directamente contra la base de datos y luego las pusimos en un script de Python.

### Pasos:

1. **Consultas SQL**:
   - Rutas más frecuentemente voladas en los últimos tres meses
   - Tasa de puntualidad de los vuelos
   - Aeropuertos de origen y destino más populares
   - Tarifas promedio por vuelo y por clase
   - Ingresos totales

2. **Crear el Dockerfile para `consultas`**:

   ```Dockerfile
   FROM python:3.8-slim

   # Instalar psycopg2 y pandas
   RUN pip install psycopg2-binary pandas

   # Crear directorio de trabajo
   WORKDIR /scripts

   # Copiar el script de Python al contenedor
   COPY consultas.py /scripts/

   # Ejecutar el script de Python
   CMD ["python", "/scripts/consultas.py"]
   ```

3. **Construir y ejecutar el contenedor `consultas`**:

   ```sh
   docker build -t consultas -f Dockerfile.consultas .
   docker run --rm --network itba-cde-cloud-architecture_default consultas
   ```
