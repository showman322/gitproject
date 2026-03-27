import psycopg2

conn = psycopg2.connect(
    dbname="phonebook_db",
    user="postgres",
    password="ltvblnzy123",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

print("Connected successfully!")