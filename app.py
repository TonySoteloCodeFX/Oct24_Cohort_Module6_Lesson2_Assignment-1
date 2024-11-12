from flask import Flask
app = Flask(__name__)
from sql_connection import connect_to_database

# @app.route('/')
# def home():
#     return 'Welcome to my Flask App'


connect = connect_to_database()
cursor = connect.cursor()

query = '''SELECT * FROM members;'''
cursor.execute(query)
show = cursor.fetchall()

print(show)
cursor.close()
connect.close()