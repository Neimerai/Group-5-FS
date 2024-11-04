from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from firebase_database import create_user, get_user_by_email, create_booking, get_bookings_by_user
import re
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure key

def is_strong_password(password):
    # Minimum length of 8 characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    # At least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    # At least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    # At least one digit
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    # At least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."

    return True, "Password is strong."

# Render the home page with full HTML structure
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")
      
        # Check for blank required fields explicitly
        if not (email and email.strip()) or not (password and password.strip()) or \
           not (first_name and first_name.strip()) or not (last_name and last_name.strip()) or \
           not (phone and phone.strip()):
            print("Error: Missing required fields")  # Debug print
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Validate password strength
        is_strong, message = is_strong_password(password)
        if not is_strong:
            return jsonify({"success": False, "message": message}), 400

        # Check if user already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            return jsonify({"success": False, "message": "Email already in use"}), 400

        # Hash password and create user
        hashed_password = generate_password_hash(password)
        user_id = create_user({
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "phone": data.get("phone"),
            "email": email,
            "password": hashed_password
        })

        return jsonify({"success": True, "message": "Signup successful", "user_id": user_id}), 200

    except Exception as e:
        print("Signup error:", str(e))  # Log the error
        return jsonify({"success": False, "message": "An error occurred during signup"}), 500



# Route to handle login (POST request)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Verify the user and check password
    user = get_user_by_email(email)
    if user and check_password_hash(user["password"], password):
        session['user_email'] = email
        return jsonify({"success": True, "message": "Login successful"})
    return jsonify({"success": False, "message": "Invalid email or password"}), 401

# Route to create a booking (POST request)
@app.route('/bookings', methods=['POST'])
def create_booking_route():
    if 'user_email' not in session:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    data = request.json
    booking_id = create_booking({
        "user_email": session['user_email'],
        "from": data.get("from"),
        "to": data.get("to"),
        "departure": data.get("departure"),
        "return_date": data.get("return_date"),
        "direct_flight": data.get("direct_flight"),
        "hotel_included": data.get("hotel_included")
    })
    return jsonify({"success": True, "message": "Booking created", "booking_id": booking_id})

# Route to get bookings for the logged-in user (GET request)
@app.route('/my_bookings', methods=['GET'])
def get_user_bookings():
    if 'user_email' not in session:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    user_email = session['user_email']
    user_bookings = get_bookings_by_user(user_email)
    return jsonify({"success": True, "bookings": user_bookings})

# Route to logout (GET request)
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_email', None)
    return jsonify({"success": True, "message": "Logged out"})

if __name__ == '__main__':
    app.run(debug=True)
