from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
	QComboBox,
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

from automationthread import AutomationThread, CURRENT_TIME


class MainWindow(QMainWindow):
	def __init__(self) -> None:
		super().__init__()

		self.setWindowTitle("PowerCampus Course Registrator")
		self.setFixedSize(720, 480)
		self.setWindowIcon(QIcon("icon.png"))

		layout: QVBoxLayout = QVBoxLayout()

		# -------------------------- WebDriver path lookup area ------------------------- #
		self.driver_label: QLabel = QLabel(
			"<h4>Select your preferred browser, and insert the path of the WebDriver corresponding to it:</h4>"
		)
		self.driver_label.setFixedHeight(15)

		self.browser_label: QLabel = QLabel("Select preferred browser:         ")
		self.browser_selector: QComboBox = QComboBox()
		self.browser_selector.addItems(["Chrome", "Edge", "Firefox"])
		self.browser_selector.currentIndexChanged.connect(self.update_driver_path)

		browser_layout: QHBoxLayout = QHBoxLayout()
		browser_layout.addWidget(self.browser_label)
		browser_layout.addStretch(1)
		browser_layout.addWidget(self.browser_selector)
		browser_layout.setStretchFactor(self.browser_selector, 8)
		browser_layout.addStretch(1)

		self.driver_path_label: QLabel = QLabel("Insert path of corresponding WebDriver:")
		self.driver_path_textbox: QLineEdit = QLineEdit()
		self.driver_path_textbox.setText("webdrivers/chromedriver/chromedriver.exe")
		self.driver_path_textbox.setPlaceholderText("WebDriver path")
		
		self.driver_path_lookup: QPushButton = QPushButton("Find WebDriver")
		self.driver_path_lookup.clicked.connect(self.lookup_driver)


		driver_path_layout: QHBoxLayout = QHBoxLayout()
		driver_path_layout.addWidget(self.driver_path_label)
		driver_path_layout.addWidget(self.driver_path_textbox)
		driver_path_layout.addWidget(self.driver_path_lookup)
		driver_path_layout.setStretchFactor(self.driver_path_textbox, 6)
		driver_path_layout.setStretchFactor(self.driver_path_lookup, 2)
		driver_path_layout.addStretch(1)

		layout.addWidget(self.driver_label)
		layout.addLayout(browser_layout)
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
	

	def update_driver_path(self, index: int) -> None:
		'''

		Slot method to update the driver path textbox when the selected browser changes.

		Args:
			index (int): the index of the element in the dropdown box. Starts at 0. 
		
		'''
		browser = self.browser_selector.itemText(index)
		if browser == 'Chrome':
			self.driver_path_textbox.setText("webdrivers/chromedriver/chromedriver.exe")
		elif browser == 'Firefox':
			self.driver_path_textbox.setText("webdrivers/geckodriver.exe")
		elif browser == 'Edge':
			self.driver_path_textbox.setText("webdrivers/msedgedriver.exe")
	

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
		browser: str = self.browser_selector.currentText()
		username: str = self.username_textbox.text()
		password: str = self.password_textbox.text()

		self.automation_thread: AutomationThread = AutomationThread(driver_path, browser, username, password)
		self.automation_thread.log_signal.connect(self.log_area.append)
		self.automation_thread.start()