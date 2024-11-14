from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from sql_connection import connect_to_database, Error

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    age = fields.Integer(required=True)

    class Meta:
        fields = ("id", "name", "age")

class WorkoutSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    member_id = fields.Integer(required=True)
    session_date = fields.String(required=True)
    session_time = fields.String(required=True)
    session_duration_minutes = fields.Integer(required=True)
    calories_burned = fields.Integer(required=True)

    class Meta:
        fields = ("id", "member_id", "session_date", "session_time", "session_duration_minutes", "calories_burned")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

@app.route('/')
def home():
    return 'Welcome to the Fitness Center Database'

@app.route('/members', methods=['GET'])
def get_members():
    try:
        connect = connect_to_database()
        if connect is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = connect.cursor(dictionary=True)

        query = '''SELECT * FROM members;'''
        cursor.execute(query)
        members = cursor.fetchall()
        return jsonify(members_schema.dump(members))
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        cursor.close()
        connect.close()

@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        connect = connect_to_database()
        if connect is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = connect.cursor()

        new_member = (member_data["name"], member_data["age"])
        query = '''
                INSERT INTO members (name, age)
                VALUES (%s, %s);
                '''
        cursor.execute(query, new_member)
        connect.commit()
        return jsonify({"Message": "New member added successfully."}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500
    
    finally:
        cursor.close()
        connect.close()
    
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        connect = connect_to_database()
        if connect is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = connect.cursor()

        updated_member = (member_data["name"], member_data["age"], id)
        query = '''
                UPDATE members
                SET name = %s, age = %s
                WHERE id = %s;
                '''
        cursor.execute(query, updated_member)
        connect.commit()
        return jsonify({"Message": "Member has been updated successfully."}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500
    
    finally:
        cursor.close()
        connect.close()

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        connect = connect_to_database()
        if connect is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = connect.cursor()

        member_to_remove = (id,)
        query1 = '''
                SELECT * FROM members
                WHERE id = %s;
                '''
        cursor.execute(query1, member_to_remove)
        member = cursor.fetchone()
        if not member:
            return jsonify({"Error": "Member not found."}), 404
        query2 = '''
                DELETE FROM members
                WHERE id = %s;
                '''
        cursor.execute(query2, member_to_remove)
        connect.commit()
        return jsonify({"Message": "Member has been deleted successfully."}), 200
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500
    
    finally:
        cursor.close()
        connect.close()

@app.route('/workouts', methods=['GET'])
def all_workouts():
    try:
        connect = connect_to_database()
        if connect is None:
            return jsonify({'Error': 'Database connection failed'}), 500
        cursor = connect.cursor(dictionary=True)

        query = '''SELECT * FROM workout_sessions;'''
        cursor.execute(query)
        workouts = cursor.fetchall()
        return jsonify(workouts_schema.dump(workouts))
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'Error': 'Internal Server Error'}), 500
    
    finally:
        cursor.close()
        connect.close()

@app.route('/workouts/<int:id>', methods=['GET'])
def all_workouts_by_id(id):
    try:
        connect = connect_to_database()
        if connect is None:
            return jsonify({'Error': 'Database connection failed'}), 500
        cursor = connect.cursor(dictionary=True)

        query = '''
                SELECT * 
                FROM workout_sessions
                WHERE member_id = %s;
                '''
        member = (id)
        cursor.execute(query, (member,))
        workouts = cursor.fetchall()
        return jsonify(workouts_schema.dump(workouts))
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'Error': 'Internal Server Error'}), 500
    
    finally:
        cursor.close()
        connect.close()

@app.route('/workouts/<int:id>', methods=['POST'])
def schedule_workout(id):
    try:
        workout_data = workout_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        connect = connect_to_database()
        if connect is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = connect.cursor()

        new_workout = (id, workout_data["session_date"], workout_data["session_time"], workout_data["session_duration_minutes"], workout_data["calories_burned"])
        query = '''
                INSERT INTO workout_sessions (member_id, session_date, session_time, session_duration_minutes, calories_burned)
                VALUES (%s, %s, %s, %s, %s);
                '''
        cursor.execute(query, new_workout)
        connect.commit()
        return jsonify({"Message": "New workout added successfully."}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500
    
    finally:
        cursor.close()
        connect.close()

@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    try:
        workout_data = workout_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        connect = connect_to_database()
        if connect is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = connect.cursor()

        updated_workout = (workout_data["member_id"], workout_data["session_date"], workout_data["session_time"], workout_data["session_duration_minutes"], workout_data["calories_burned"], id)
        query = '''
                UPDATE workout_sessions
                SET member_id = %s, session_date = %s, session_time = %s, session_duration_minutes = %s, calories_burned = %s
                WHERE id = %s;
                '''
        cursor.execute(query, updated_workout)
        connect.commit()
        return jsonify({"Message": "Workout has been updated successfully."}), 200
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Internal Server Error"}), 500
    
    finally:
        cursor.close()
        connect.close()
        