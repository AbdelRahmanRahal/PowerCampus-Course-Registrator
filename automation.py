from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from exceptions import *

class PowerCampusAutomation:

	def __init__(self, driver_path: str) -> None:
		# Initialising the WebDriver.
		self.driver: Chrome = Chrome(service = Service(driver_path))

		# Initialising the waits and their durations.
		self.wait: WebDriverWait = WebDriverWait(self.driver, 30)
		self.alert_wait: WebDriverWait = WebDriverWait(self.driver, 1)


	def login(self, username: str, password: str) -> None:
		# Opening the login page.
		self.driver.get('https://register.nu.edu.eg/PowerCampusSelfService/Home/LogIn')

		# Entering username.
		username_field: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, 'txtUsername')))
		username_field.send_keys(username)
		
		# Clicking the next button.
		login_button: WebElement = self.driver.find_element(By.ID, 'btnNext')
		login_button.click()

		# Checking if the page produced an error.
		try:
			page_alert: WebElement = self.alert_wait.until(EC.presence_of_element_located((By.ID, 'pageAlert')))
			raise InvalidUsername
		except TimeoutException:
			pass

		# Entering password.
		password_field: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, 'txtPassword')))
		password_field.send_keys(password)

		# Clicking the login button.
		login_button: WebElement = self.driver.find_element(By.ID, 'btnSignIn')
		login_button.click()

		# Checking if the page produced an error.
		try:
			page_alert: WebElement = self.alert_wait.until(EC.presence_of_element_located((By.ID, 'pageAlert')))
			raise InvalidPassword
		except TimeoutException:
			pass


	def register(self) -> None:
		# Opening the course registration page.
		self.driver.get('https://register.nu.edu.eg/PowerCampusSelfService/Registration/Courses')

		# Clicking the register button.
		register_button: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, 'btnRegister')))
		register_button.click()


	def quit(self) -> None:
		# Closing the driver once done.
		self.driver.quit()