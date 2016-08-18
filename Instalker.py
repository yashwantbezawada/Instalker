#!/usr/bin/env python

"""Instalker.py: Download all the images of the Instagramers who are followed by user."""

__author__		=	"Yashwant Bezawada"
__version__		=	"1.4"
__maintainer__		=	"Yashwant Bezawada"
__email__		=	"yashwant_b@me.com"
__status__		=	"Beta"


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display
from selenium.webdriver.common.action_chains import *
from bs4 import BeautifulSoup
import getpass
import urllib
import time
import sys
import os

#print "Installing Requirements"

#print "Provide your Super User Password if asked for"

#os.system("sudo pip install selenium")
#os.system("sudo pip install pyvirtualdisplay")
#os.system("sudo apt-get install xvfb xserver-xephyr")

display = Display(visible=0, size=(1920, 1920))
display.start()

driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get('https://www.instagram.com/')
print "Connecting to Instagram....."
time.sleep(5)
driver.implicitly_wait(10)
driver.find_element_by_link_text("Log in").click()
usrid = raw_input('Enter your Instagram User ID: ')
pswd = getpass.getpass('Enter your Instagram Password:')
inputEmail = driver.find_element_by_xpath("/html/body/span[@id='react-root']/section[@class='_8f735']/main[@class='_6ltyr _rnpza']/article[@class='_60k3m']/div[@class='_p8ymb']/div[@class='_nvyyp'][1]/div[@class='_uikn3']/form[@class='_rwf8p']/div[@class='_ccek6 _i31zu'][1]/input[@class='_kp5f7 _qy55y']")
inputEmail.send_keys(usrid)
inputPass = driver.find_element_by_xpath("/html/body/span[@id='react-root']/section[@class='_8f735']/main[@class='_6ltyr _rnpza']/article[@class='_60k3m']/div[@class='_p8ymb']/div[@class='_nvyyp'][1]/div[@class='_uikn3']/form[@class='_rwf8p']/div[@class='_ccek6 _i31zu'][2]/input[@class='_kp5f7 _qy55y']")
inputPass.send_keys(pswd)
inputPass.submit()
print "Logging in ........"
try:
	driver.find_element_by_css_selector("a[href*='/yashwant_b/']").click()
except Exception:
	print "Invalid Username/Password"
	print "Exiting....."
	exit()
num_fol = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a/span').text
num_fol = int(num_fol)

print "You are following "+ str(num_fol)+" members"

driver.find_element_by_css_selector("a[href*='/yashwant_b/following/']").click()

oldSize = 0
newSize = 0
driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li[1]/div/div[1]/div/div[2]').click()
for j in range(1,50):
	driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li[1]/div/div[1]/div/div[2]').send_keys(Keys.ARROW_DOWN)
newSize = len(driver.find_elements_by_tag_name('li'))

print "Scanning everyone you are following...."

while newSize > oldSize:
	oldSize = newSize
	for j in range(1,20):
		driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li[1]/div/div[1]/div/div[2]').send_keys(Keys.ARROW_DOWN)
	time.sleep(3)
	newSize = len(driver.find_elements_by_tag_name('li'))
print "Scanned "+str(num_fol)+" members"
####################################################################################################################
for i in range(1,num_fol+1):
	usr_url = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/ul/li["+str(i)+"]/div/div/div/div/a").get_attribute("href")
	driver.implicitly_wait(20)
	body = driver.find_element_by_tag_name("body")
	body.send_keys(Keys.CONTROL + 't')
	driver.implicitly_wait(20)

	driver.get(usr_url)

	usr_id = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/div[1]/h1').text

	path = usr_id
	print usr_id

	if not os.path.exists(path):
		os.mkdir(path)

	while True:
		try:
			driver.find_element_by_link_text("Load more").click()
		except NoSuchElementException:
			break

	oldSize = 0
	newSize = 0

	driver.execute_script("window.scrollTo(0,document.body.scrollHeight)");
	newSize = len(driver.find_elements_by_tag_name('img'))

	while newSize > oldSize:
		oldSize = newSize
		for k in range(1,5):
			for l in range(1,3):
				driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
			time.sleep(1)
			for l in range(1,3):
				driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/div[1]/h1').send_keys(Keys.PAGE_UP)
			time.sleep(1)
		newSize = len(driver.find_elements_by_tag_name('img'))
	print "Total of "+str(newSize)+" images and videos"

	images = driver.find_elements_by_tag_name('img')
	count = 0
	for image in images:
    		src = image.get_attribute("src")
		tmp_name = src
		tmp_name = str(tmp_name)
		tmp_name = tmp_name.replace('/', '_')
		if src:
			if not os.path.exists(path+"/"+tmp_name+".jpg"):
				count = count + 1
				try:
        				urllib.urlretrieve(src,path+"/"+tmp_name+".jpg")
				except Exception,e:
					print e
					try:
						time.sleep(2)
        					urllib.urlretrieve(src,path+"/"+tmp_name+".jpg")
						continue	
					except Exception,f:
						print f
						continue
				print "Downloading image "+str(count)
			else:
				print "Skipping already saved on drive"
	body = driver.find_element_by_tag_name("body")
	body.send_keys(Keys.CONTROL + 'w')
driver.quit()
display.stop()
