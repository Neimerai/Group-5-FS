import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Initialize WebDriver
service = Service("C:\\Users\\Nicholas Wang\\Documents\\chromedriver-win32\\chromedriver.exe")  # Path to ChromeDriver
driver = webdriver.Chrome(service=service)

# Flask app URL
BASE_URL = "http://127.0.0.1:5000"

def generate_random_email():
    """Generates a random email address for testing."""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{username}@example.com"


def test_signup_and_login_flow():
    try:
        # Generate random email and set password
        random_email = generate_random_email()
        password = "StrongP@ssw0rd"

        # Navigate to the home page
        driver.get(BASE_URL)

        # Click the Log In button to open the login modal
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "login-button"))
        )
        login_button.click()
        print("Login modal opened.")

        # Wait for the sign-up link in the login modal and click it
        signup_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Create a new account"))
        )
        signup_link.click()
        print("Sign-up modal opened.")

        # Wait for the sign-up modal to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "registerPopup"))
        )

        # Fill out the sign-up form
        driver.find_element(By.ID, "first-name").send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "sign-up-email").send_keys(random_email)
        driver.find_element(By.ID, "phone").send_keys("1234567890")
        driver.find_element(By.ID, "sign-up-password").send_keys(password)
        driver.find_element(By.ID, "terms").click()
        print("Sign-up form filled.")

        # Submit the form explicitly
        signup_form = driver.find_element(By.ID, "registerForm")
        signup_form.submit()
        print("Sign-up form submitted.")

        # Handle the alert that appears after signup
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Alert detected: {alert.text}")
        alert.accept()  # Accept the alert
        print("Registration successful accepted.")

        # Wait for the login modal to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "loginPopup"))
        )

        # Fill in the email field with the newly created email
        driver.find_element(By.ID, "email").send_keys(random_email)
        driver.find_element(By.ID, "password").send_keys(password)
        print("Login form filled.")

        # Submit the login form
        login_submit_button = driver.find_element(By.CLASS_NAME, "signup-button")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "signup-button"))
        )
        login_submit_button.click()
        print("Login button clicked.")

         # Handle the alert that appears after signup
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Alert detected: {alert.text}")
        alert.accept()  # Accept the alert
        print("Login successful accepted.")

    except TimeoutException as e:
        print(f"Test signup and login flow: Timeout occurred: {e}")
    except Exception as e:
        print(f"Test signup and login flow: Failed ({e})")
    finally:
        driver.quit()


# Run the test
test_signup_and_login_flow()
