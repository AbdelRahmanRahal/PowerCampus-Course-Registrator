'''

Copyright (c) 2023, AbdelRahman Rahal
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the same directory as this file.

'''
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, Firefox, Edge
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from exceptions import InvalidPassword, InvalidUsername

class PowerCampusAutomation:
	'''
	
	Course registration automation script class.

	'''
	def __init__(self, driver_path: str, browser: str) -> None:
		'''
		
		Course registration automation script class. 

		Ags:
			driver_path (str): the path of the WebDriver specified by the user.
			browser (str): the user's preferred browser.
		
		'''
		# Matching the driver with the browser.
		match browser:
			case "Chrome":
				self.driver = Chrome(service = ChromeService(driver_path))
			case "Firefox":
				self.driver = Firefox(service = FirefoxService(driver_path))
			case  "Edge":
				# Use Edge WebDriver
				self.driver = Edge(service = EdgeService(driver_path))

		# Initialising the waits and their durations.
		self.wait: WebDriverWait = WebDriverWait(self.driver, 30)
		self.alert_wait: WebDriverWait = WebDriverWait(self.driver, 1)


	def login(self, username: str, password: str) -> None:
		'''
		
		Method responsible for logging into PowerCampus.

		Args:
			username (str): the username of the user on PowerCampus.
			password (str): the password of the user on PowerCampus.
		
		'''
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
		'''
		
		Method responsible for registering the selected courses on PowerCampus.

		'''
		# Opening the course registration page.
		self.driver.get('https://register.nu.edu.eg/PowerCampusSelfService/Registration/Courses')

		# Clicking the register button.
		register_button: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, 'btnRegister')))
		register_button.click()


	def quit(self) -> None:
		'''
		
		Method responsible for closing the driver once done.

		'''
		self.driver.quit()