import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate('config/group-5---fs-firebase-adminsdk-uvff6-a24fe4531e.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://group-5---fs-default-rtdb.firebaseio.com/'
})

# Database references
users_ref = db.reference('users')
bookings_ref = db.reference('bookings')

def create_user(user_data):
    try:
        new_user_ref = users_ref.push()  # Pushes a new user to the 'users' node
        new_user_ref.set(user_data)      # Sets user_data at this new reference
        print("User created with Firebase key:", new_user_ref.key)  # Debug print
        return new_user_ref.key
    except Exception as e:
        print("Error creating user:", e)
        return None
    
def get_user_by_email(email):
    try:
        snapshot = users_ref.order_by_child('email').equal_to(email).get()
        print("Snapshot retrieved:", snapshot)  # Debug print
        
        if snapshot:
            user_id, user_data = next(iter(snapshot.items()))  # Get the first matching user
            print("User found:", user_data)  # Debug print
            return {**user_data, "user_id": user_id}
        print("No user found with email:", email)
        return None
    except Exception as e:
        print("Error retrieving user by email:", e)
        return None


# Function to create a new booking
def create_booking(booking_data):
    try:
        new_booking_ref = bookings_ref.push()
        new_booking_ref.set(booking_data)
        return new_booking_ref.key
    except Exception as e:
        print("Error creating booking:", e)
        return None

# Function to get bookings by user ID
def get_bookings_by_user(user_id):
    try:
        snapshot = bookings_ref.order_by_child('userId').equal_to(user_id).get()
        return snapshot if snapshot else {}
    except Exception as e:
        print("Error retrieving bookings for user:", e)
        return {}

# Function to update a booking
def update_booking(booking_id, new_data):
    try:
        booking_ref = bookings_ref.child(booking_id)
        booking_ref.update(new_data)
        print("Booking updated successfully")
    except Exception as e:
        print("Error updating booking:", e)

# Function to delete a booking
def delete_booking(booking_id):
    try:
        bookings_ref.child(booking_id).delete()
        print("Booking deleted successfully")
    except Exception as e:
        print("Error deleting booking:", e)
