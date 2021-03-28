# This is a simple script which you can use without proxies
from account_creator import AccountCreator

if __name__ == '__main__':
   	signup_site = input('Enter the site you want to create an account for: ')

   	ac = AccountCreator(url=signup_site)

   	ac.enterData()
   	
   	ac.close() # Call this at the end of your script to close all browser instances