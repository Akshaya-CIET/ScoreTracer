#including desired packages/libraries
import requests
from bs4 import BeautifulSoup
import pynotify
from time import sleep
import sys
import signal
import configparser

ll=[]     #empty list to store the matches list

def set_config(list):
	'''to store the url of the live matches and to track the url's list'''
	config = configparser.ConfigParser()                    #creates an obj for the class configparser
	j=0
	for i in list:
		if j<=len(list):
			config['URLS'] = {j : i}                        #to store the urls in the form of key,value pair
			j=j+1
			with open('urllist.conf', 'a') as configfile:   #to open the specified file in append mode 
				config.write(configfile)                    #to write the contents into the file


def sendmessage(title,message):
	'''to print the score message of the selected match which will be stored in title'''
	print title.upper()
	print "SCORE:::::",message                              #prints the score
	return;


global user_input
global soup       
list_links = []                                             #empty list

def get_url():    
	'''to get the source code for the given webpage'''
	print 'Live Cricket Matches:'
	print '='*len('Live Cricket Matches:')
	url = "http://static.cricinfo.com/rss/livescores.xml"   #the xml file to get the matches held list
	sc = requests.get(url)                                  #gets the url's source code
	soup = BeautifulSoup(sc.text,'lxml')                    #parses the xml file
	return soup                 

def find_matches(soup2):
	'''to find the live matches list and to find those respective url and store it in an list'''
	i = 1
	for data in soup2.findAll('item'):                      #finds all the blocks with name item
		print str(i)+'.'+data.find('description').text      #description has the match title
		i += 1                                              #increments the i value
  
	for link in soup2.findAll('item'):                      #finds tags with values item
		list_links.append(link.find('guid').text)           #finds the links of the respective websites and appends to list
	return list_links

def select_match(ll):
	'''ask the user to enter the match number for which the scores to be displayed and act according to the choice'''
	print 'Enter match number or enter 0 to exit: '  
	while True:
		try:
			global user_input
			user_input=int(input("Choice:::"))              #gets input from user

		except NameError as n:                              #exception call for NameError
			print n,'\nEnter correct input::'
			continue
		except SyntaxError as s:                            #exception call for syntax error
			print s,'\nEnter correct input::'
		except (KeyboardInterrupt,SystemExit):              #exception call for keyboard interrupt
			signal.signal(signal.SIGINT, signal_handler())
			while True:
				time.sleep(1)
		if user_input < 0 or user_input > 30:               #user input cannot be a negative number
			print 'Enter correct input:: (between 0 and 30)' 
			continue
		elif user_input == 0:                               #user input equal to 0 
			sys.exit()
		elif user_input>len(ll):                            #user input becomes greater than length of the match list
			print 'Enter the correct input (less than ',len(ll),')'
			continue               
		else:
			break 
	return user_input

def signal_handler():
	'''to exit the program if the excution needs to be terminated'''
	sys.exit(0)

def getchoice():
	'''get the choice from the user'''
	try:     
		ch=input("Do you want to display Live scores(1) or Exit(2) ?:::::: ")            #get the choice
	except (KeyboardInterrupt,SystemExit):                                               #exception call
		signal.signal(signal.SIGINT, signal_handler())
		while True:
			time.sleep(1)
	return ch

def switch_choice(ch):
	'''to print the live scores'''
	if ch==1:
		live_score()
	elif ch==2:
		print "User wanted to exit:::::"
		exit(1)
	elif ch==0 or ch>2:
		try:
			print ":::Enter a valid choice:::"
			getchoice()
		except (KeyboardInterrupt,SystemExit):                                   #exception to handle keyboard interrupt such as pressing ctrl+c
			signal.signal(signal.SIGINT, signal_handler())
			while True:
				time.sleep(1)

def live_score():
	while True:
			url = list_links[user_input - 1]                                     #the xml file to get the matches held list
			sc = requests.get(url)                                               #gets the url's source code
			soup = BeautifulSoup(sc.text,'lxml')                                 #parses the xml file
			score = soup.findAll('title')       
			try:
				sc.raise_for_status()                                            #check for the network connection
			except Exception as exc:                                             #exception call
				 print ('Connection Issue') 
				 continue 
			try:   
				sendmessage('LIVE SCORES',score[0].text)                         #function call
				sleep(30)                                                        #Set time accordingly.
			except (KeyboardInterrupt,SystemExit):
				signal.signal(signal.SIGINT, signal_handler())
				while True:
					time.sleep(1)


if __name__=="__main__":
	''' loading the source code file as the main program'''
	try:
		soup1=get_url()                                  #calls the function get_url and stores the return value in the variable
		ll=find_matches(soup1)                           #calls the function find_matches and stores list of matches in the variable in ll
		set_config(ll)                                   #calls the funtion set_config(ll) to write the urls in conf file
		b=select_match(ll)                               #calls the function select_match() and stores the return value in the variable b
		ch=getchoice()                                   #calls the function get_choice() to get user input in b
		switch_choice(ch)                                #performs the user specified task
		url = list_links[b-1]                            #gets the link needed for user 
		sc = requests.get(url)                           #gets the url's source code
		soup = BeautifulSoup(sc.text,'lxml')             #parses the source code
		getchoice()
	except (KeyboardInterrupt,SystemExit):               #to handle keyboard interrupt exceptions
		signal.signal(signal.SIGINT,signal_handler())
		while True:
			time.sleep(1)

