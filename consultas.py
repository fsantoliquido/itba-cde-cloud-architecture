import psycopg2
import pandas as pd

def get_connection():
    conn = psycopg2.connect(
        host="db",
        database="airlines",
        user="fsantoliquido",
        password="itba1234"
    )
    print("Conexión exitosa.")
    return conn

def execute_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    print("Ejecutando query...")
    try:
        cursor.execute(query)
        print("Query ejecutada.")
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        print(f"Resultados obtenidos: {len(results)} filas.")
        return pd.DataFrame(results, columns=columns)
    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return pd.DataFrame()
    finally:
        cursor.close()
        conn.close()

def main():
    queries = {
        "Rutas más frecuentemente voladas en los últimos 30 días (supuesto: hoy es 15 de Agosto de2017) ": """
        SELECT f.departure_airport, f.arrival_airport, COUNT(*) AS flight_count
        FROM flights f
        WHERE f.scheduled_departure >= cast('2017-08-15' as date) - INTERVAL '30 DAYS'
        GROUP BY 1,2
        ORDER BY flight_count DESC;
        """,
        "Tasa de puntualidad de los vuelos en los últimos tres meses (supuesto: hoy es 15 de Agosto de2017)": """
        SELECT COUNT(CASE WHEN actual_arrival <= scheduled_arrival THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) AS on_time_percentage,
               COUNT(CASE WHEN actual_arrival > scheduled_arrival THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) AS delayed_percentage
        FROM flights
        WHERE scheduled_departure >= cast('2017-08-15' as date) - INTERVAL '3 months';
        """,
        "Aeropuertos de origen y destino más populares en los últimos tres meses(supuesto: hoy es 15 de Agosto de2017)": """
        SELECT departure_airport, arrival_airport, COUNT(*) AS flight_count
        FROM flights
        WHERE scheduled_departure >= cast('2017-08-15' as date) - INTERVAL '3 months'
        GROUP BY 1,2
        ORDER BY flight_count DESC;
        """,
        "Tarifas promedio por clase en los últimos tres meses(supuesto: hoy es 15 de Agosto de2017)": """
        SELECT tf.fare_conditions, AVG(tf.amount) AS avg_fare
        FROM ticket_flights tf
        JOIN flights f ON tf.flight_id = f.flight_id
        WHERE f.scheduled_departure >= cast('2017-08-15' as date) - INTERVAL '3 months'
        GROUP BY 1
        ORDER BY tf.fare_conditions;
        """,
        "Revenue por mes en USD": """
        SELECT CAST(DATE_TRUNC('Month',book_date) AS DATE) AS book_month, SUM(total_amount) as total_rev 
        FROM bookings
        GROUP BY 1
        ;
        """
    }

    for title, query in queries.items():
        print(f"\nEjecutando consulta: {title}")
        df = execute_query(query)
        print(f"Resultados de la consulta: {title}")
        if not df.empty:
            print(df)
        else:
            print("No se obtuvieron resultados o hubo un error en la consulta.")

if __name__ == "__main__":
    main()