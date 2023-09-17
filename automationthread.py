'''

Copyright (c) 2023, AbdelRahman Rahal
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the same directory as this file.

'''
import time
from datetime import datetime, timedelta

from PySide6.QtCore import QThread, Signal
from selenium.common.exceptions import (
	ElementClickInterceptedException,
	NoSuchDriverException,
	SessionNotCreatedException,
	TimeoutException
)

from automation import PowerCampusAutomation
from exceptions import InvalidPassword, InvalidUsername


def CURRENT_TIME() -> str:
	'''
	
	Returns:
		str: the current time in 12-hour format in a small font.
	
	'''
	return datetime.now().strftime("<small>[%I:%M %p]</small>")


class AutomationThread(QThread):
	'''
	
	Class made to execute the automation script and handle any errors that arise from it.

	'''
	button_state_signal: Signal = Signal()
	log_signal: Signal = Signal(str)


	def __init__(self, driver_path: str, browser: str, username: str, password: str) -> None:
		'''
		
		Class made to execute the automation script and handle any errors that arise from it.

		Args:
			driver_path (str): the path for the desired WebDriver.
			username (str): the username of the user on PowerCampus.
			password (str): the password of the user on PowerCampus.
		
		'''
		super().__init__()

		self.driver_path: str = driver_path
		self.browser: str = browser
		self.username: str = username
		self.password: str = password


	def run(self) -> None:
		'''

		This method gets called when the thread starts (i.e. `___.start()`).
		It's responsible for executing the automation script and keeping it in order.

		'''
		loop: bool = True
		while loop:
			try:
				loop = False

				# -------------------------- Initialising WebDriver -------------------------- #
				self.log_signal.emit(
					f"{CURRENT_TIME()} ⚙️ Initialising WebDriver..."
				)
				start_time: float = time.time()
				automation: PowerCampusAutomation = PowerCampusAutomation(self.driver_path, self.browser)
				end_time: float = time.time()
				elapsed_time: float = end_time - start_time # Calculating the time it took to initialise the WebDriver.
				self.log_signal.emit(
					f"{CURRENT_TIME()} ✅ WebDriver initialised successfully. [<small>{elapsed_time:.2f}s</small>]"
				)

				# -------------------------------- Signing in -------------------------------- #
				self.log_signal.emit(
					f"{CURRENT_TIME()} ⚙️ Signing in..."
				)
				start_time: float = time.time()
				automation.login(self.username, self.password)
				end_time: float = time.time()
				elapsed_time: float = end_time - start_time # Calculating the time it took to sign in.
				self.log_signal.emit(
					f"{CURRENT_TIME()} ✅ Signed in successfully. [<small>{elapsed_time:.2f}s</small>]"
				)

				# Giving the page time to sign in and process.
				time.sleep(5)

				# ---------------------------- Registering courses --------------------------- #
				self.log_signal.emit(
					f"{CURRENT_TIME()} ⚙️ Registering courses..."
				)
				start_time: float = time.time()
				automation.register()
				end_time: float = time.time()
				elapsed_time: float = end_time - start_time # Calculating the time it took to register the courses.
				self.log_signal.emit(
					f"{CURRENT_TIME()} ✅ Registered successfully. [<small>{elapsed_time:.2f}s</small>]"
				)

				# ----------------------- Safely closing the WebDriver ----------------------- #
				self.log_signal.emit(
					f"{CURRENT_TIME()} ⚙️ Closing WebDriver..."
				)
				automation.quit()
				self.log_signal.emit(
					f"{CURRENT_TIME()} ✅ Closed WebDriver."
				)
			except NoSuchDriverException:
				self.log_signal.emit(
					f"{CURRENT_TIME()} ❌ WebDriver corrupted, incompatible, unobtainable, or doesn't exist."
				)
			except OSError:
				self.log_signal.emit(
					f"{CURRENT_TIME()} ❌ WebDriver selected is invalid."
				)
			except SessionNotCreatedException as e:
				self.log_signal.emit(
					f"{CURRENT_TIME()} ❌ Could not initialise WebDriver for the following reason(s): {e.msg}"
				)
			except TimeoutException:
				self.log_signal.emit(
					f"{CURRENT_TIME()} ❌ WebDriver unexpectedly terminated, "
					"possibly due to a connection error or an unexpected change to the site."
				)
			except InvalidUsername:
				self.log_signal.emit(
					f"{CURRENT_TIME()} ❌ Invalid username. Closing WebDriver..."
				)
				self.log_signal.emit(
					f"{CURRENT_TIME()} ✅ Closed WebDriver."
				)
			except InvalidPassword:
				self.log_signal.emit(
					f"{CURRENT_TIME()} ❌ Invalid password. Closing WebDriver..."
				)
				self.log_signal.emit(
					f"{CURRENT_TIME()} ✅ Closed WebDriver."
				)
			except ElementClickInterceptedException:
				self.log_signal.emit(
					f"{CURRENT_TIME()} ⚠️ Registration period hasn't started. Closing WebDriver..."
				)
				automation.quit() # pyright: ignore[reportUnboundVariable]
				self.log_signal.emit(
					f"{CURRENT_TIME()} ✅ Closed WebDriver."
				)
				self.log_signal.emit(
					f"{CURRENT_TIME()} ℹ️ Trying again at "
					f"{(datetime.now() + timedelta(minutes = 5)).strftime('%I:%M %p')}. "
					"Keep this window open."
				)

				loop = True
				time.sleep(300) # 5 minutes
			finally:
				# Re-enabling the run button.
				self.button_state_signal.emit()