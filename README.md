
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
