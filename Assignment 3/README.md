How to run the TESTS for assignment 3:
1. Ensure you are in the "app" folder
2. run "python test_app.py"
3. If 6 all tests passed, then the system works

The tests done were:
1. Test Case Name: User registration form validation
    Objective: Registration checks for valid inputs.
    Action: Leave any of the fields blank or enter an invalid format.
    Assert: The system should display an error message.

2. Test Case Name: Password strength validation
    Objective: Ensure that the system checks for password strength during registration.
    Action: Enter a weak password and submit the form.
    Assert: The system should display a message indicating that the password is too weak.

3. Test Case Name: Successful registration submission
    Objective: Users can submit with valid input.
    Action: Enter valid names, email, phone number, password, then click sign up.
    Assert: The system should redirect the user to a login page.

4. Test Case Name: Login form validation
    Objective: Validates user inputs before submission.
    Action: Enter an invalid email format and/or incorrect password, then click login
    Assert: The system should display an error message.

5. Test Case Name: Successful login submission
    Objective: Make sure users are able to log in.
    Action: Enter a valid email and password, then click login
    Assert: The user is redirected to the searching page.

6. Test Case Name: Display booking confirmation
    Objective: Verify that a confirmation page is displayed with the correct booking
    reference after a payment is completed.
    Action: Complete the booking process and proceed to the confirmation page.
    Assert: The system should display a booking reference number, flight details, and a
    "Thank you for your booking" message.

