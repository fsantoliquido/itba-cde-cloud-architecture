import psycopg2
import os

def main():
    print("Conectando a la base...")
    """
    La función se conecta a la db airlines. Toma del archivo "demo-small-en..." los dato y los inserta en las tablas. Luego se commitean los cmabios.
    Por ultimo se cierra la conexión
    """

    conn = psycopg2.connect(
        host="db",
        database="airlines",
        user="fsantoliquido",
        password="itba1234"
    )
    print("Conexión exitosa.")
    cur = conn.cursor()
    
    print("Leo el archivo SQL...")
    
    with open('/scripts/transformed_inserts.sql', 'r') as file:
        sql = file.read()
    
    print("Ejecuto sentencias batch por faltamemoria...")
    
    statements = sql.split(';')
    batch_size = 100  # Tamaño del batch
    batch = []

    for statement in statements:
        if statement.strip():
            batch.append(statement)
            if len(batch) >= batch_size:
                try:
                    cur.execute(';'.join(batch))
                    conn.commit()
                    print(f"Batch de {batch_size} ejecutado")
                except psycopg2.Error as e:
                    print(f"Error al ejecutar batch: {e}")
                batch = []
    

    if batch:
        try:
            cur.execute(';'.join(batch))
            conn.commit()
            print("Sentencias que no soninsert ejecutadas")
        except psycopg2.Error as e:
            print(f"Error al ejecutar: {e}")

    print("Cierro la la conexión..")

    cur.close()
    conn.close()
    print("Finalizado con éxito")

if __name__ == "__main__":
    main()