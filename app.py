from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import fields
from sql_connection import connect_to_database
app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    age = fields.Integer(required=True)

    class Meta:
        fields = ("id", "name", "age")


member_schema = MemberSchema()

# @app.route('/')
# def home():
#     return 'Welcome to my Flask App'


# connect = connect_to_database()
# cursor = connect.cursor()

# query = '''SELECT * FROM members;'''
# cursor.execute(query)
# show = cursor.fetchall()

# print(show)
# cursor.close()
# connect.close()