# Account Creator

This is a simple python script which can be imported into other programs to help either create random, bogus data or enter data into a website provided. The websites are opened using Firefox and selenium, this is so that the script is semi-automatic, if anything needs to be done manually it can be done.

#### Features:
- You can use proxies with the script to evade IP blocks
- Generate email addresses from 10minutemail, this will remain open so access to the inbox is available
- The script is semi-automatic, so you can evade captures easily just by manually clicking them if needed

#### Requirements:
- Need python 3.7 or above
- Need geckodriver for selenium to use Firefox ([link to download](https://github.com/mozilla/geckodriver/releases "link to download")), make sure this is in your path or in the same folder as *account_creator.py*
- Install any requirements for the script using `pip install -r requirements.txt`

##### Optional:
 - To use proxies with the script, you can easily install the http_request_randomizer module using `pip install http-request-randomizer` ([link to pypi page](https://pypi.org/project/http-request-randomizer/ "link to pypi page"))

------------


#### Examples:
##### 1:
 ```python
 # This is a simple script which you can use without proxies
	from account_creator import AccountCreator

	if __name__ == '__main__':
		signup_site = input('Enter the site you want to create an account for: ')

		ac = AccountCreator(url=signup_site)

		ac.enterData()
		
		ac.close()
```
##### 2:
```python
# This is a simple script which fetches a proxy and uses it to access a website
from account_creator import AccountCreator
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

if __name__ == '__main__':
	signup_site = input('Enter the site you want to create an account for: ')

	req_proxy = RequestProxy()
	proxies = req_proxy.get_proxy_list()
	proxies = [proxy for proxy in req_proxy.get_proxy_list() if proxy.country == 'United Kingdom']
	proxyStr = proxies[0].get_address()

	ac = AccountCreator(proxyStr=proxyStr, url=signup_site)

	ac.enterData()
	
	ac.close()
```

------------


#### TODO:
1. Allow the use of chrome
2. Allow custom name file for name generation
3. Add other cool stuff
