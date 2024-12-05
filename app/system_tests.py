import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# Flask app URL
BASE_URL = "http://127.0.0.1:5000"

def generate_random_email():
    """Generates a random email address for testing."""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{username}@example.com"

def test_user_flow():
    try:
        # Login in/Sign up test
        # Generate random email and set password
        random_email = generate_random_email()
        password = "StrongP@ssw0rd"

        # Navigate to the home page
        driver.get(BASE_URL)
        print("Navigated to home page.")

        # Click the Log In button to open the login modal
        login_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "login-button"))
        )
        login_button.click()
        print("Login modal opened.")

        # Wait for the sign-up link in the login modal and click it
        signup_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Create a new account"))
        )
        signup_link.click()
        print("Sign-up modal opened.")

        # Fill out the sign-up form
        wait.until(EC.visibility_of_element_located((By.ID, "registerPopup")))
        driver.find_element(By.ID, "first-name").send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "sign-up-email").send_keys(random_email)
        driver.find_element(By.ID, "phone").send_keys("1234567890")
        driver.find_element(By.ID, "sign-up-password").send_keys(password)
        driver.find_element(By.ID, "terms").click()
        print("Sign-up form filled.")

        # Submit the form explicitly
        driver.find_element(By.ID, "registerForm").submit()
        print("Sign-up form submitted.")

        # Handle the alert that appears after signup
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Signup Alert: {alert.text}")
        alert.accept()
        print("Signup successful.")

        # Wait for the login modal to be visible
        wait.until(EC.visibility_of_element_located((By.ID, "loginPopup")))
        driver.find_element(By.ID, "email").send_keys(random_email)
        driver.find_element(By.ID, "password").send_keys(password)
        print("Login form filled.")

        # Fill in the email field with the newly created email
        login_submit_button = driver.find_element(By.CLASS_NAME, "signup-button")
        login_submit_button.click()
        print("Login form submitted.")

        # Submit the login form
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Login Alert: {alert.text}")
        alert.accept()
        print("Login successful.")

        # Booking test
        wait.until(EC.visibility_of_element_located((By.ID, "flightForm")))
        print("Booking form is visible.")

        # Fill out the booking form
        driver.find_element(By.ID, "from").send_keys("Toronto Pearson International (YYZ)")
        driver.find_element(By.ID, "to").send_keys("Los Angeles International (LAX)")
        driver.find_element(By.ID, "departure").send_keys("2024-12-10")
        driver.find_element(By.ID, "return").send_keys("2024-12-15")
        print("Booking form filled.")

        # Select checkboxes for booking options
        direct_flight_checkbox = driver.find_element(By.ID, "direct-flight")
        hotel_included_checkbox = driver.find_element(By.ID, "hotel-included")

        if not direct_flight_checkbox.is_selected():
            direct_flight_checkbox.click()
        if not hotel_included_checkbox.is_selected():
            hotel_included_checkbox.click()
        print("Checkboxes selected.")

        # Submit the booking form
        submit_button = driver.find_element(By.CLASS_NAME, "search-button")
        submit_button.click()
        print("Booking form submitted.")

        # Handle the alert that appears after booking
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Booking Alert: {alert.text}")

        if "Booking created successfully" in alert.text:
            print("Booking creation test passed.")
        else:
            raise AssertionError(f"Unexpected alert text: {alert.text}")

        alert.accept()

        # Logout test
        logout_button = driver.find_element(By.CLASS_NAME, "login-button")
        logout_button.click()
        print("Logout button clicked.")

        # Handle the alert that appears after logout
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Logout Alert: {alert.text}")

        if "Logged out" in alert.text:
            print("Logout test passed.")
        else:
            raise AssertionError(f"Unexpected logout alert text: {alert.text}")

        alert.accept()

    except TimeoutException as e:
        print(f"Timeout Error: {e}")
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        driver.quit()

# Run the test
test_user_flow()
