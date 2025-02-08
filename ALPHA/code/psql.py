import psycopg2


# conn = psycopg2.connect(dbname='selectel', user='selectel', 
#                         password='selectel', host='82.202.136.203', port=5432)
# cursor = conn.cursor()

def insert_into_table(leaders):
    conn = psycopg2.connect(dbname='selectel', user='selectel', 
                        password='selectel', host='82.202.136.203', port=5432)
    cursor = conn.cursor()

    sorted_leaderboard = sorted(leaders.items(), key=lambda x: x[1][1], reverse=True)
    for nickname, points in sorted_leaderboard:
        cursor.execute('INSERT INTO players (nickname, points_classic, points_modern, points_genius) VALUES (%s, %s, %s, %s)', 
                       (nickname, points[0], points[1], points[2]))
        conn.commit()
    
    conn.close()

def get_data_from_table():
    conn = psycopg2.connect(dbname='selectel', user='selectel', 
                        password='selectel', host='82.202.136.203', port=5432)
    cursor = conn.cursor()
    data = {}
    cursor.execute('SELECT * FROM players')
    for row in cursor:
        row = row[1:]
        data[row[0]] = [row[1], row[2], row[3]] 
    return data
