import time
from datetime import datetime, timedelta

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
	QFileDialog,
	QHBoxLayout, 
	QLabel,
	QLineEdit,
	QMainWindow,
	QPushButton, 
	QTextEdit,
	QVBoxLayout,
	QWidget
)
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchDriverException, TimeoutException

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
	log_signal: Signal = Signal(str)


	def __init__(self, driver_path: str, username: str, password: str) -> None:
		'''
		
		Class made to execute the automation script and handle any errors that arise from it.

		Args:
			driver_path (str): the path for the desired WebDriver.
			username (str): the username of the user on PowerCampus.
			password (str): the password of the user on PowerCampus.
		'''
		super().__init__()

		self.driver_path: str = driver_path
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
				automation: PowerCampusAutomation = PowerCampusAutomation(self.driver_path)
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


class MainWindow(QMainWindow):
	def __init__(self) -> None:
		super().__init__()

		self.setWindowTitle("PowerCampus Course Registrator")
		self.resize(720, 480)
		self.setWindowIcon(QIcon("icon.png"))

		layout: QVBoxLayout = QVBoxLayout()

		# -------------------------- WebDriver path lookup area ------------------------- #
		self.driver_label: QLabel = QLabel(
			"<h4>Select path for WebDriver (preferably ChromeDriver):</h4>"
		)
		self.driver_label.setFixedHeight(15)

		self.driver_path_textbox: QLineEdit = QLineEdit()
		self.driver_path_textbox.setText("chromedriver/chromedriver.exe")
		self.driver_path_textbox.setPlaceholderText("ChromeDriver Path")
		
		self.driver_path_lookup: QPushButton = QPushButton("Find WebDriver")
		self.driver_path_lookup.clicked.connect(self.lookup_driver)


		driver_path_layout: QHBoxLayout = QHBoxLayout()
		driver_path_layout.addWidget(self.driver_path_textbox)
		driver_path_layout.addWidget(self.driver_path_lookup)
		driver_path_layout.setStretchFactor(self.driver_path_textbox, 3)
		driver_path_layout.addStretch(1)

		layout.addWidget(self.driver_label)
		layout.addLayout(driver_path_layout)

		# ---------------------- Username and password textboxes --------------------- #
		self.login_label: QLabel = QLabel(
			"<h4>Fill out your Nile University PowerCampus sign-in information:</h4>"
		)
		self.login_label.setFixedHeight(15)

		self.username_label: QLabel = QLabel("Username:     ")
		self.username_textbox: QLineEdit = QLineEdit()
		self.username_textbox.setPlaceholderText("Username")

		username_layout: QHBoxLayout = QHBoxLayout()
		username_layout.addWidget(self.username_label)
		username_layout.addWidget(self.username_textbox)
		username_layout.setStretchFactor(self.username_textbox, 3)
		username_layout.addStretch(1)


		self.password_label: QLabel = QLabel("Password:      ")
		self.password_textbox: QLineEdit = QLineEdit()
		self.password_textbox.setPlaceholderText("Password")
		self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)

		password_layout: QHBoxLayout = QHBoxLayout()
		password_layout.addWidget(self.password_label)
		password_layout.addWidget(self.password_textbox)
		password_layout.setStretchFactor(self.password_textbox, 3)
		password_layout.addStretch(1)


		layout.addWidget(self.login_label)
		layout.addLayout(username_layout)
		layout.addLayout(password_layout)

		# ------------------------------- Run button ------------------------------ #
		self.run_button: QPushButton = QPushButton("Run")
		self.run_button.setFixedWidth(100)
		self.run_button.clicked.connect(self.run_automation)
		layout.addWidget(self.run_button, alignment= Qt.AlignmentFlag.AlignHCenter)

		# --------------------------------- Log area --------------------------------- #
		self.log_area: QTextEdit = QTextEdit()
		self.log_area.setReadOnly(True)
		self.log_area.setFixedHeight(150)
		layout.addWidget(self.log_area)

		# ---------------------- Containerising the main layout ---------------------- #
		container: QWidget = QWidget()
		container.setLayout(layout)
		container.setContentsMargins(15, 15, 15, 15)

		self.setCentralWidget(container)
	

	def lookup_driver(self) -> None:
		'''
		
		Method responsible for the WebDriver lookup window.

		'''
		file_path, _ = QFileDialog.getOpenFileName(self, "Select WebDriver")
		if file_path:
			self.driver_path_textbox.clear()
			self.driver_path_textbox.setText(file_path)
		else:
			
			self.log_area.append(
				f"{CURRENT_TIME()} ℹ️ No file was selected."
			)


	def run_automation(self) -> None:
		'''
		
		The method that gets called when the user presses the "Run" button.
		It takes all the info the user entered and sends it to the `AutomationThread`.

		'''
		driver_path: str = self.driver_path_textbox.text()
		username: str = self.username_textbox.text()
		password: str = self.password_textbox.text()

		self.automation_thread: AutomationThread = AutomationThread(driver_path, username, password)
		self.automation_thread.log_signal.connect(self.log_area.append)
		self.automation_thread.start()