import psycopg2

con = psycopg2.connect(
  database="postgres",
  user="postgres",
  password="pass123",
  host="127.0.0.1",
  port="5432"
)

print("Database opened successfully")