class InvalidUsername(Exception):
	def __init__(self) -> None:
		'''
		Base class for staticvar exceptions.

		Args:
			message (str): error message.
		'''
		super().__init__()


class InvalidPassword(Exception):
	def __init__(self) -> None:
		'''
		Base class for staticvar exceptions.

		Args:
			message (str): error message.
		'''
		super().__init__()