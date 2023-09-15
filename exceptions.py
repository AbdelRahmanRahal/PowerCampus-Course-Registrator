class InvalidUsername(Exception):
	def __init__(self) -> None:
		'''
		
		Exception class raised when the page gives an error when the user enters an invalid username.
		'''
		super().__init__()


class InvalidPassword(Exception):
	def __init__(self) -> None:
		'''
		
		Exception class raised when the page gives an error when the user enters an invalid password.

		'''
		super().__init__()