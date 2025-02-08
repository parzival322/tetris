import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def insert_into_table(leaders):
    conn = psycopg2.connect(dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                        password=os.getenv('PASSWORD'), host=os.getenv('HOST'), port=os.getenv('PORT'))
    cursor = conn.cursor()

    sorted_leaderboard = sorted(leaders.items(), key=lambda x: x[1][1], reverse=True)
    for nickname, points in sorted_leaderboard:
        cursor.execute('INSERT INTO players (nickname, points_classic, points_modern, points_genius) VALUES (%s, %s, %s, %s)', 
                       (nickname, points[0], points[1], points[2]))
        conn.commit()
    
    conn.close()

def get_data_from_table():
    conn = psycopg2.connect(dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                        password=os.getenv('PASSWORD'), host=os.getenv('HOST'), port=os.getenv('PORT'))
    cursor = conn.cursor()
    data = {}
    cursor.execute('SELECT * FROM players')
    for row in cursor:
        row = row[1:]
        data[row[0]] = [row[1], row[2], row[3]] 
    return data
