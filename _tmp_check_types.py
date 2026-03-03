from django.db import connection
with connection.cursor() as cur:
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME")
    for row in cur.fetchall():
        print(row[0])
