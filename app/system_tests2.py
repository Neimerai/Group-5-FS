from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Flask app URL
BASE_URL = "http://127.0.0.1:5000"



def test_create_booking():
    try:
        # Navigate to the home page
        driver.get(BASE_URL)

        # Log in to an existing account (use test credentials)
        driver.find_element(By.CLASS_NAME, "login-button").click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "loginPopup"))
        )
        driver.find_element(By.ID, "email").send_keys("testuser@example.com")
        driver.find_element(By.ID, "password").send_keys("StrongP@ssw0rd")
        driver.find_element(By.CLASS_NAME, "signup-button").click()

        # Wait for login success
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

        # Fill the booking form
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flightForm"))
        )
        driver.find_element(By.ID, "from").send_keys("Toronto Pearson International (YYZ)")
        driver.find_element(By.ID, "to").send_keys("Los Angeles International (LAX)")
        driver.find_element(By.ID, "departure").send_keys("2024-12-10")
        driver.find_element(By.ID, "return").send_keys("2024-12-15")

        # Scroll checkboxes into view and click
        direct_flight_checkbox = driver.find_element(By.ID, "direct-flight")
        hotel_included_checkbox = driver.find_element(By.ID, "hotel-included")
        
        driver.execute_script("arguments[0].scrollIntoView(true);", direct_flight_checkbox)
        ActionChains(driver).move_to_element(direct_flight_checkbox).click().perform()
        
        driver.execute_script("arguments[0].scrollIntoView(true);", hotel_included_checkbox)
        ActionChains(driver).move_to_element(hotel_included_checkbox).click().perform()

        # Submit the booking
        driver.find_element(By.CLASS_NAME, "search-button").click()

        # Wait for booking success alert
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        assert "Booking created successfully!" in alert.text
        alert.accept()
        print("Booking creation test passed.")

    except TimeoutException as e:
        print(f"Test create booking: Timeout occurred: {e}")
    except Exception as e:
        print(f"Test create booking: Failed ({e})")
    finally:
        driver.quit()

# Run the test
test_create_booking()
