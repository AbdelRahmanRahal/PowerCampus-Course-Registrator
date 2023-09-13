from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QFileDialog
import sys


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("PowerCampus Course Registrator")
		self.resize(720, 480)

		layout: QVBoxLayout = QVBoxLayout()

		# -------------------------- Driver path lookup area ------------------------- #
		self.driver_label: QLabel = QLabel('Select path for webdriver (preferably ChromeDriver):')
		self.driver_label.setFixedHeight(15)

		self.driver_path_textbox: QLineEdit = QLineEdit()
		self.driver_path_textbox.setText('chromedriver/chromedriver.exe')
		self.driver_path_textbox.setPlaceholderText("ChromeDriver Path")
		

		self.driver_path_lookup: QPushButton = QPushButton("Find Driver")
		self.driver_path_lookup.clicked.connect(self.select_file)


		driver_path_layout: QHBoxLayout = QHBoxLayout()

		driver_path_layout.addWidget(self.driver_path_textbox)
		driver_path_layout.addWidget(self.driver_path_lookup)
		driver_path_layout.addStretch(1)
		driver_path_layout.setStretchFactor(self.driver_path_textbox, 3)

		layout.addWidget(self.driver_label)
		layout.addLayout(driver_path_layout)

		# ---------------------- Username and password textboxes --------------------- #
		self.username_textbox: QLineEdit = QLineEdit()
		self.username_textbox.setPlaceholderText("Username")
		layout.addWidget(self.username_textbox)

		self.password_textbox: QLineEdit = QLineEdit()
		self.password_textbox.setPlaceholderText("Password")
		self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)
		layout.addWidget(self.password_textbox)

		# ------------------------------- Submit button ------------------------------ #
		self.submit_button: QPushButton = QPushButton("Submit")
		self.submit_button.clicked.connect(self.submit)
		layout.addWidget(self.submit_button)

		# --------------------------------- Log area --------------------------------- #
		self.log_area: QTextEdit = QTextEdit()
		self.log_area.setReadOnly(True)
		self.log_area.setFixedHeight(150)
		layout.addWidget(self.log_area)

		container: QWidget = QWidget()
		container.setLayout(layout)
		container.setContentsMargins(15, 15, 15, 15)

		self.setCentralWidget(container)

	def select_file(self):
		file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
		self.log_area.append(f"File selected: {file_path}")

	def submit(self):
		self.log_area.append(f"Username: {self.username_textbox.text()}, Password: {self.password_textbox.text()}")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()