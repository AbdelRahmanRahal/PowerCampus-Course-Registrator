import sys, time
from datetime import datetime

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
	QApplication,
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
from selenium.common.exceptions import NoSuchDriverException

from automation import PowerCampusAutomation


def CURRENT_TIME():
	return datetime.now().strftime("<small>[%I:%M %p]</small>")


class AutomationThread(QThread):
	log_signal = Signal(str)


	def __init__(self, driver_path, username, password):
		super().__init__()
		self.driver_path = driver_path
		self.username = username
		self.password = password


	def run(self) -> None:
		'''
		This method gets called when the thread starts (i.e. `___.start()`)
		'''
		try:
			self.log_signal.emit(
				f"{CURRENT_TIME()} ⚙️ Initialising WebDriver..."
			)
			start_time = time.time()
			automation = PowerCampusAutomation(self.driver_path)
			end_time = time.time()
			elapsed_time = end_time - start_time
			self.log_signal.emit(
				f"{CURRENT_TIME()} ✅ WebDriver initialised successfully. (Took {elapsed_time:.2f}s)"
			)

			automation.login(self.username, self.password)
			automation.register()
			automation.quit()
		except NoSuchDriverException:
			self.log_signal.emit(
				f"{CURRENT_TIME()} ❌ WebDriver corrupted, incompatible, unobtainable, or doesn't exist."
			)
		except OSError:
			self.log_signal.emit(
				f"{CURRENT_TIME()} ❌ WebDriver selected is invalid."
			)


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("PowerCampus Course Registrator")
		self.resize(720, 480)
		self.setWindowIcon(QIcon("icon.png"))

		layout: QVBoxLayout = QVBoxLayout()

		# -------------------------- Driver path lookup area ------------------------- #
		self.driver_label: QLabel = QLabel(
			"<h4>Select path for WebDriver (preferably ChromeDriver):</h4>"
		)
		self.driver_label.setFixedHeight(15)

		self.driver_path_textbox: QLineEdit = QLineEdit()
		self.driver_path_textbox.setText("chromedriver/chromedriver.exe")
		self.driver_path_textbox.setPlaceholderText("ChromeDriver Path")
		
		self.driver_path_lookup: QPushButton = QPushButton("Find Driver")
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
			"<h4>Fill out your Nile University PowerCampus login information:</h4>"
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
	

	def lookup_driver(self):
		file_path, _ = QFileDialog.getOpenFileName(self, "Select WebDriver")
		if file_path:
			self.driver_path_textbox.clear()
			self.driver_path_textbox.setText(file_path)
		else:
			
			self.log_area.append(
				f"{CURRENT_TIME()} ℹ️ No file was selected."
			)


	def run_automation(self):
		driver_path = self.driver_path_textbox.text()
		username = self.username_textbox.text()
		password = self.password_textbox.text()

		self.automation_thread = AutomationThread(driver_path, username, password)
		self.automation_thread.log_signal.connect(self.log_area.append)
		self.automation_thread.start()
	


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()