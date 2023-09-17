'''

Copyright (c) 2023, AbdelRahman Rahal
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the same directory as this file.

'''
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