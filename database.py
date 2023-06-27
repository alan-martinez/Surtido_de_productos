import mysql.connector

def establecer_conexion():
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="productos_problema"
    )
    
    return conexion
