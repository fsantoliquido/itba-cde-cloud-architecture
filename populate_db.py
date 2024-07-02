import psycopg2
import os

def main():
    print("Conectando a la base de datos PostgreSQL...")
    # Conectar a la base de datos PostgreSQL
    conn = psycopg2.connect(
        host="db",  # Nombre del servicio del contenedor PostgreSQL en docker-compose.yml
        database="airlines",
        user="fsantoliquido",
        password="itba1234"
    )
    print("Conexión exitosa.")
    cur = conn.cursor()
    
    print("Leyendo el archivo SQL...")
    # Leer el archivo SQL
    with open('/scripts/transformed_inserts.sql', 'r') as file:
        sql = file.read()
    
    print("Ejecutando sentencias SQL en lotes...")
    # Ejecutar el archivo SQL en lotes
    statements = sql.split(';')
    batch_size = 100  # Tamaño del lote
    batch = []

    for statement in statements:
        if statement.strip():
            batch.append(statement)
            if len(batch) >= batch_size:
                try:
                    cur.execute(';'.join(batch))
                    conn.commit()
                    print(f"Lote de {batch_size} sentencias ejecutado.")
                except psycopg2.Error as e:
                    print(f"Error al ejecutar lote: {e}")
                batch = []
    
    # Ejecutar cualquier sentencia restante
    if batch:
        try:
            cur.execute(';'.join(batch))
            conn.commit()
            print("Sentencias restantes ejecutadas.")
        except psycopg2.Error as e:
            print(f"Error al ejecutar lote final: {e}")

    print("Cerrando la conexión...")
    # Cerrar la conexión
    cur.close()
    conn.close()
    print("Finalizado con éxito.")

if __name__ == "__main__":
    main()