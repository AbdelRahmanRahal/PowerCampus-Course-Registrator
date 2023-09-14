from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class PowerCampusAutomation:
	def __init__(self, driver_path):
		self.driver = webdriver.Chrome(service= Service(driver_path))


	def login(self, username, password):
		# Open the website
		self.driver.get('https://register.nu.edu.eg/PowerCampusSelfService/Home/LogIn')

		# Enter username
		username_field = self.driver.find_element(By.ID, 'username_field_id')
		username_field.send_keys(username)

		# Enter password
		password_field = self.driver.find_element(By.ID, 'password_field_id')
		password_field.send_keys(password)

		# Click the login button
		login_button = self.driver.find_element(By.ID, 'login_button_id')
		login_button.click()


	def register(self):
		# Open the website
		self.driver.get('https://register.nu.edu.eg/PowerCampusSelfService/Home/LogIn')

		# Find the register button using the Xpath and click it
		register_button = self.driver.find_element(By.XPATH, '//xpath/of/register/button')
		register_button.click()


	def quit(self):
		# Close the driver once done
		self.driver.quit()