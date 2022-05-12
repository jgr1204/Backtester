import psycopg2 as psql
from dotenv import dotenv_values


config = dotenv_values(".env")
db = psql.connect(dbname="nba", user=config.get("user"), password=config.get("pword"), host="3.239.122.35")