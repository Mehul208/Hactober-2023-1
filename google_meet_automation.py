from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

''' 
	Main Program variables and functions
'''

opt = None
caps = None
driver = None
meeting_code = None
class_time = None


def set_code(meet_code, tm):
	global meeting_code, class_time
	class_time = tm
	meeting_code = meet_code	


def browser_options():
	global opt, caps
	opt = ChromeOptions()
	opt.add_argument("--disable-infobars")
	opt.add_argument("--disable-extensions")
	opt.add_argument('--ignore-certificate-errors')
	opt.add_argument('--ignore-ssl-errors')
	opt.add_argument('start-maximized')
	caps = webdriver.DesiredCapabilities.CHROME.copy()
	caps['acceptInsecureCerts'] = True	# Function to add browser arguments


def start_browser():
	global driver
	driver = webdriver.Chrome(desired_capabilities=caps, options=opt)
	driver.get("https://meet.google.com/")
	WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
	tn = driver.title.lower()
	if "sign in - google accounts" in tn:
		login()
	elif "meet" in tn:
		join_class()
	else:
		print("Error code 44")	# Function to Start Browser


def login():
	verify_tag = driver.find_element_by_class_name('PrDSKc').get_attribute('innerText')
	verify_to = "To help keep your account secure, Google needs to verify it’s you. Please sign in again to continue."
	if verify_tag == verify_to:
		next_btn = driver.find_element_by_class_name('VfPpkd-RLmnJb')
		next_btn.click()
		time.sleep(4)
		type_input('whsOnd', password)
		driver.find_element_by_class_name('VfPpkd-RLmnJb').click()
		WebDriverWait(driver,timeout=10).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
		if "Meet" in driver.title:
			join_class()
		else:
			print("Exit at 63 not in meet >> "+driver.title)
	else:
		print(verify_tag)	# Function to Login


def join_class():
	time.sleep(3)
	driver.find_element_by_class_name('ox9SMb').click() # Join btn on home screen
	time.sleep(1)
	type_input('poFWNe', meeting_code)
	get_btn("l4V7wb",2).click()
	if WebDriverWait(driver,10000).until(EC.title_contains(meeting_code)):
		conct_call()
	else:
		print("It worked, not in meet at 66")	#Function to Join Class with Meeting Code


def conct_call():
	time.sleep(2)
	get_btn("U26fgb", 0).click()
	get_btn("U26fgb",1).click()
	time.sleep(2)
	join_btn = get_btn('Fxmcue',0)
	join_btn.click()
	time.sleep(class_time+160)
	get_btn("U26fgb", 2).click()
	time.sleep(2)
	driver.close()	#Function to Connct Call with Default Settings


def get_btn(btn_class, element_num):
	btn =  driver.find_elements_by_class_name(btn_class)
	return btn[element_num]	#Function to Get Buttons or elements


def type_input(class_name, type_string):
	x = driver.find_element_by_class_name(class_name)
	x.click()
	time.sleep(1)
	x.send_keys(type_string)	#Function to type in input with class name


'''
	Program Starts with, Call to start browser and
	custom browser options
'''

browser_options()
