import mysql.connector
class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = "localhost",
            port= 3306,
            user = "root",
            password = "root",
            database = "mydb"
        )
        self.cursor = self.connection.cursor()
    
    