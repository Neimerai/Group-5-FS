import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

BASE_URL = "http://127.0.0.1:5000"

def generate_random_email():
    """Generates a random email address for testing."""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{username}@example.com"

def test_signup_login_booking():
    try:
        random_email = generate_random_email()
        password = "StrongP@ssw0rd"

        driver.get(BASE_URL)
        print("Navigated to home page.")

        login_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "login-button"))
        )
        login_button.click()
        print("Login modal opened.")

        signup_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Create a new account"))
        )
        signup_link.click()
        print("Sign-up modal opened.")

        wait.until(EC.visibility_of_element_located((By.ID, "registerPopup")))
        driver.find_element(By.ID, "first-name").send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "sign-up-email").send_keys(random_email)
        driver.find_element(By.ID, "phone").send_keys("1234567890")
        driver.find_element(By.ID, "sign-up-password").send_keys(password)
        driver.find_element(By.ID, "terms").click()
        print("Sign-up form filled.")

        driver.find_element(By.ID, "registerForm").submit()
        print("Sign-up form submitted.")

        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Signup Alert: {alert.text}")
        alert.accept()
        print("Signup successful.")

        wait.until(EC.visibility_of_element_located((By.ID, "loginPopup")))
        driver.find_element(By.ID, "email").send_keys(random_email)
        driver.find_element(By.ID, "password").send_keys(password)
        print("Login form filled.")

        login_submit_button = driver.find_element(By.CLASS_NAME, "signup-button")
        login_submit_button.click()
        print("Login form submitted.")

        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Login Alert: {alert.text}")
        alert.accept()
        print("Login successful.")

        wait.until(EC.visibility_of_element_located((By.ID, "flightForm")))
        print("Booking form is visible.")

        driver.find_element(By.ID, "from").send_keys("Toronto Pearson International (YYZ)")
        driver.find_element(By.ID, "to").send_keys("Los Angeles International (LAX)")
        driver.find_element(By.ID, "departure").send_keys("2024-12-10")
        driver.find_element(By.ID, "return").send_keys("2024-12-15")
        print("Booking form filled.")

        direct_flight_checkbox = driver.find_element(By.ID, "direct-flight")
        hotel_included_checkbox = driver.find_element(By.ID, "hotel-included")

        if not direct_flight_checkbox.is_selected():
            direct_flight_checkbox.click()
        if not hotel_included_checkbox.is_selected():
            hotel_included_checkbox.click()
        print("Checkboxes selected.")

        submit_button = driver.find_element(By.CLASS_NAME, "search-button")
        submit_button.click()
        print("Booking form submitted.")

        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Booking Alert: {alert.text}")

        if "Booking created successfully" in alert.text:
            print("Booking creation test passed.")
        else:
            raise AssertionError(f"Unexpected alert text: {alert.text}")

        alert.accept()

    except TimeoutException as e:
        print(f"Timeout Error: {e}")
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        driver.quit()

test_signup_login_booking()
