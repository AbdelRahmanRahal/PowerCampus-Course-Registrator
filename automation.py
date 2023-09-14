from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class PowerCampusAutomation:
	def __init__(self, driver_path):
		self.driver = webdriver.Chrome(service= Service(driver_path))
		# Initialising the wait and its duration
		self.wait = WebDriverWait(self.driver, 30)


	def login(self, username, password):
		# Open the website
		self.driver.get('https://register.nu.edu.eg/PowerCampusSelfService/Home/LogIn')

		# Enter username
		username_field = self.wait.until(EC.presence_of_element_located((By.ID, 'txtUsername')))
		username_field.send_keys(username)
		
		# Click the next button
		login_button = self.driver.find_element(By.ID, 'btnNext')
		login_button.click()

		# Enter password
		password_field = self.wait.until(EC.presence_of_element_located((By.ID, 'txtPassword')))
		password_field.send_keys(password)

		# Click the login button
		login_button = self.driver.find_element(By.ID, 'btnSignIn')
		login_button.click()


	def register(self):
		# Open the website
		self.driver.get('https://register.nu.edu.eg/PowerCampusSelfService/Registration/Courses')

		# Find the register button using the Xpath and click it
		register_button = self.wait.until(EC.presence_of_element_located((By.ID, 'btnRegister')))
		register_button.click()


	def quit(self):
		# Close the driver once done
		self.driver.quit()