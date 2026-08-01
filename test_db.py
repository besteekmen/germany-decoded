from psycopg import connect

conn = connect(
    host="localhost",
    port=5432,
    dbname="germany_decoded",
    user="admin",
    password="password",
)

print("Connected!")

conn.close()