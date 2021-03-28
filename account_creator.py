import logging
import random
import secrets
import string
import time

from colorama import Fore, init
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


class AccountCreator:
	def __init__(self, proxyStr=None, url=None, _logging=False):
		"""This is the method which is called when the object in initilised.

		Args:
			proxyStr (String, optional): A string fo the proxy ip and port to be used (ip:port). Defaults to None.
			url (String, optional): A string of the website to access. Defaults to None.
			_logging (Bool, optional): A boolean to determine if selenium logs should be displayed or not. Defaults to False.
		"""

		init(autoreset=True)

		if not _logging:
			logger = logging.getLogger('selenium.webdriver.remote.remote_connection') # To disable selenium logging unless logging=True
			logger.propagate = False

		if proxyStr:
			self.proxyObj = Proxy({
				'proxyType': ProxyType.MANUAL,
				'httpProxy': proxyStr,    
				'sslProxy': proxyStr,    
			})
		else:
			self.proxyObj = None

		self.url = url
		if self.url:
			self.driver = webdriver.Firefox(proxy=self.proxyObj) if self.proxyObj else webdriver.Firefox()
			self.driver.get(url)
		self.email_driver = None

	def getEmail(self): # Gets a burner email from 10minutemail, window stays open incase inbox is needed.
		self.email_driver = webdriver.Firefox(proxy=self.proxyObj) if self.proxyObj else webdriver.Firefox()
		self.email_driver.get("https://10minutemail.com/")

		time.sleep(2)

		email = self.email_driver.find_element_by_id('mail_address').get_attribute('value')

		return email

	def generateData(self, age=None): # Generates name, username, password, birthday and email data.
		current_year = 2021

		with open('names.txt', 'r') as f:
			names = [name.strip() for name in f.readlines()]

		name = random.choice(names)
		first_name = name.split()[0]
		last_name = name.split()[1]
		username = f'{first_name}_{last_name}{random.randint(1000, 9999)}'
		password = f'{random.choice(string.ascii_uppercase)}_{secrets.token_hex(4)}'
		birthday = f'{random.randint(1, 12)}-{random.randint(0, 28)}-{(current_year - age) if age else random.randint(1950, current_year - 19)}'
		email = self.getEmail()

		with open('accounts.txt', 'a') as f:
			f.write(f'[{time.strftime("%H:%M:%S", time.localtime())}] {first_name} {last_name}, {username}, {email}, {password}, {birthday}\n')

		print(f'{Fore.GREEN}Generated data and saved to file: {first_name} {last_name}, {username}, {email}, {password}, {birthday}')

		return first_name, last_name, username, password, birthday, email

	def enterData(self, age=None): # Tries to enter data into a form
		if not self.url:
			print(f'{Fore.RED}Please initilise this class with a url supplied if you want to enter data into a form')
			return

		if age:
			data = self.generateData(age)
		else:
			data = self.generateData()

		first_name_list = ['fname', 'firstname', 'first_name', 'register-fname', 'firstName']
		last_name_list = ['lname', 'lastname', 'last_name', 'register-lname', 'lastName']
		username_list = ['username', 'user_name', 'uname', 'userName', 'register-uname']
		password_list = ['password', 'passwd', 'pass', 'passWord', 'register-pword', 'pword']
		confirm_password_list = ['confirm_passowrd', 'confirm_passwd', 'confirm_pass', 'confirmPassword', 'confirmPasswd', 'confirmPass', 'password2', 'passwd2', 'pass2']
		email_list = ['email', 'mail', 'register-email']

		lists = [
			(first_name_list, data[0], f'{Fore.RED}Could not find space to enter the first name'),
			(last_name_list, data[1], f'{Fore.RED}Could not find space to enter the last name'),
			(username_list, data[2], f'{Fore.RED}Could not find space to enter the username'),
			(password_list, data[3], f'{Fore.RED}Could not find space to enter the password'),
			(confirm_password_list, data[3], f'{Fore.RED}Could not find space to enter the confirmation password'),
			(email_list, data[5], f'{Fore.RED}Could not find space to enter the email'),
		]

		for data_type in lists:
			for idx, item in enumerate(data_type[0]):
				try:
					self.driver.find_element_by_id(item).send_keys(data_type[1])
					break
				except: pass

				try:
					self.driver.find_element_by_name(item).send_keys(data_type[1])
					break
				except: pass
			else:
				print(data_type[2])
			
		print(f'{Fore.GREEN}Please enter the birthdate manually: {data[4]}')

	def close(self): # Closes all drivers if they are open
		if url:
			self.driver.close()
		if self.email_driver:
			self.email_driver.close()

		