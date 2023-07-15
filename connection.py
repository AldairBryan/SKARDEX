import mysql.connector
class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = "localhost",
            port= 8088,
            user = "root",
            password = "qwerty",
            database = "turista_feliz"
        )
        self.cursor = self.connection.cursor()