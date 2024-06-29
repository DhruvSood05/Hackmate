from flask import Flask, request, jsonify
import mysql.connector

# Create a Flask application
app = Flask(__name__)

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="tiger",  
    database="hackmate_db"  
)
cursor = db.cursor()

# Define a route for the root URL
@app.route('/')
def index():
    return 'Welcome to HackMate!'

# Define endpoint for user registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    
    try:
        # Insert user into MySQL
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        values = (username, password, email)
        cursor.execute(query, values)
        db.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to register user', 'error': str(e)}), 500

# Define endpoint for user login
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    try:
        # Check user credentials in MySQL
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        
        if user:
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'message': 'Failed to log in', 'error': str(e)}), 500

# Endpoint for profile retrieval
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        # Fetch user profile from MySQL
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        
        if user:
            profile = {
                'username': user[1],
                'email': user[2]
                # Add more fields as needed
            }
            return jsonify(profile), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve profile', 'error': str(e)}), 500

# Endpoint for profile update
@app.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.get_json()
    new_username = data.get('username')
    new_email = data.get('email')
    
    try:
        # Update user profile in MySQL
        update_query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
        update_values = (new_username, new_email, user_id)
        cursor.execute(update_query, update_values)
        db.commit()
        
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update profile', 'error': str(e)}), 500

# Endpoint for swiping actions

@app.route('/swipe', methods=['POST'])
def swipe_action():
    data = request.get_json()
    swiper_id = data['swiper_id']
    swipee_id = data['swipee_id']
    action = data['action']  # 'like' or 'dislike'
    
    # Insert swipe action into MySQL
    try:
        query = "INSERT INTO swipe_history (swiper_id, swiped_id, action) VALUES (%s, %s, %s)"
        values = (swiper_id, swipee_id, action)
        cursor.execute(query, values)
        db.commit()
        
        return jsonify({'message': 'Swipe action recorded'}), 201
    except mysql.connector.Error as err:
        app.logger.error(f"Error recording swipe action: {err}")
        return jsonify({'message': f'Failed to record swipe action: {err}'}), 500

# Endpoint for retrieving matches
# Endpoint for retrieving matches
@app.route('/matches/<int:user_id>', methods=['GET'])
def get_matches(user_id):
    # Fetch matches from MySQL based on user_id
    query = """
            SELECT DISTINCT u.username, u.email
            FROM users u
            JOIN swipe_history s1 ON u.id = s1.swiped_id
            JOIN swipe_history s2 ON u.id = s2.swiper_id
            WHERE s1.swiper_id = %s 
              AND s2.swiped_id = %s 
              AND s1.action = 'like' 
              AND s2.action = 'like'
            """
    cursor.execute(query, (user_id, user_id))
    matches = cursor.fetchall()
    
    matched_users = []
    for match in matches:
        matched_profile = {
            'username': match[0],
            'email': match[1]
        }
        matched_users.append(matched_profile)
    
    return jsonify(matched_users), 200

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
