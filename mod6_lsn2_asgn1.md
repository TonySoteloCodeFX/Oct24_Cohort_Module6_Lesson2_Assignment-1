<h2>Module 6 Lesson 2: Assignment | Building RESTFul APIs</h2>
<hr>

<h4>1. Managing a Fitness Center Database</h4>

<b>Objective:</b> The aim of this assignment is to develop a Flask application to manage a fitness center's database, focusing on interacting with the Members and WorkoutSessionstables. This will enhance your skills in building RESTful APIs using Flask, handling database operations, and implementing CRUD functionalities.

<h5><i><u>Task 1: Setting Up the Flask Environment and Database Connection</u></i></h5>

- Create a new Flask project and set up a virtual environment.
<br>

- Install necessary packages like Flask, Flask-Marshmallow, and MySQL connector.
<br>

- Establish a connection to your MySQL database. - Use the Members and WorkoutSessions tables used on previous Lessons
<br>

  <b>Expected Outcome:</b> A Flask project with a connected database and the required tables created.

<h5><i><u>Task 2: Implementing CRUD Operations for Members</u></i></h5>

 - Create Flask routes to add, retrieve, update, and delete members from the Memberstable.
<br>

 - Use appropriate HTTP methods: POST for adding, GET for retrieving, PUT for updating, and DELETE for deleting members.
<br>

 - Ensure to handle any errors and return appropriate responses.
<br>
  
   <b>Expected Outcome:</b> Functional endpoints for managing members in the database with proper error handling.
   <br>

   <b>Code Example:</b>

```
   @app.route('/members', methods=['POST'])
def add_member():
    # Logic to add a member
    pass

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    # Logic to retrieve a member
    pass

# other routes to update and delete
```
<b>NOTE:</b> Make sure you have ALL of the CRUD operations implemented, not just the two above.

<h5><i><u>Task 3: Managing Workout Sessions</u></i></h5>

- Develop routes to schedule, update, and view workout sessions.
<br>

- Implement a route to retrieve all workout sessions for a specific member.
<br>

  <b>Expected Outcome:</b> A comprehensive set of endpoints for scheduling and viewing workout sessions, with the ability to retrieve detailed information about each session.

 

