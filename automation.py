from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from exceptions import *

class PowerCampusAutomation:
	def __init__(self, driver_path):
		self.driver = webdriver.Chrome(service = Service(driver_path))
		# Initialising the waits and their durations
		self.wait = WebDriverWait(self.driver, 30)
		self.alert_wait = WebDriverWait(self.driver, 1)


	def login(self, username, password):
		# Open the website
		self.driver.get('https://register.nu.edu.eg/PowerCampusSelfService/Home/LogIn')

		# Enter username
		username_field = self.wait.until(EC.presence_of_element_located((By.ID, 'txtUsername')))
		username_field.send_keys(username)
		
		# Click the next button
		login_button = self.driver.find_element(By.ID, 'btnNext')
		login_button.click()

		# Checking if the page produced an error
		try:
			page_alert = self.alert_wait.until(EC.presence_of_element_located((By.ID, 'pageAlert')))
			raise InvalidUsername
		except TimeoutException:
			pass

		# Enter password
		password_field = self.wait.until(EC.presence_of_element_located((By.ID, 'txtPassword')))
		password_field.send_keys(password)

		# Click the login button
		login_button = self.driver.find_element(By.ID, 'btnSignIn')
		login_button.click()

		# Checking if the page produced an error
		try:
			page_alert = self.alert_wait.until(EC.presence_of_element_located((By.ID, 'pageAlert')))
			raise InvalidPassword
		except TimeoutException:
			pass


	def register(self):
		# Open the website
		self.driver.get('https://register.nu.edu.eg/PowerCampusSelfService/Registration/Courses')

		# Find the register button using its ID and clicking it
		register_button = self.wait.until(EC.presence_of_element_located((By.ID, 'btnRegister')))
		register_button.click()


	def quit(self):
		# Close the driver once done
		self.driver.quit()