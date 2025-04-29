import mysql.connector 

def buat_database_jika_belum_ada():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS item_db")
    print(" Database item_db dicek / dibuat otomatis")
    cursor.close()
    conn.close()

buat_database_jika_belum_ada()
