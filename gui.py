from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QFileDialog
import sys


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("PowerCampus Course Registrator")
		self.resize(720, 480)
		self.setWindowIcon(QIcon('icon.png'))

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
		driver_path_layout.setStretchFactor(self.driver_path_textbox, 3)
		driver_path_layout.addStretch(1)

		layout.addWidget(self.driver_label)
		layout.addLayout(driver_path_layout)

		# ---------------------- Username and password textboxes --------------------- #
		self.login_label: QLabel = QLabel('Fill out your Nile University PowerCampus login information:')
		self.login_label.setFixedHeight(15)

		self.username_label: QLabel = QLabel('Username:     ')
		self.username_textbox: QLineEdit = QLineEdit()
		self.username_textbox.setPlaceholderText("Username")

		username_layout: QHBoxLayout = QHBoxLayout()
		username_layout.addWidget(self.username_label)
		username_layout.addWidget(self.username_textbox)
		username_layout.setStretchFactor(self.username_textbox, 3)
		username_layout.addStretch(1)


		self.password_label: QLabel = QLabel('Password:      ')
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
		self.run_button.clicked.connect(self.run)
		layout.addWidget(self.run_button, alignment= Qt.AlignmentFlag.AlignHCenter)

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

	def run(self):
		self.log_area.append(f"Username: {self.username_textbox.text()}, Password: {self.password_textbox.text()}")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()