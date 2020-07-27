#!/usr/bin/python
#-------------------------------------------------------------------------------------------------------------------------
# MySignals SW Cloud API Library 
# Author:Theodore Flokos
# For: TIE LAB
#-------------------------------------------------------------------------------------------------------------------------
#Import needed libraries
import requests,json,datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display

#MySignals Object Definition
class mysignals(object):
	#Initiate mysignals class variables
	def __init__(self,email,password):
		#Starndard Headers
		headers = {
			'Content-Type':'application/x-www-form-urlencoded',
			'Accept': 'application/x.webapi.v1+json',
			}
		#Base Url for MySignals Cloud API Backend
		self.base_url = 'https://api.libelium.com/mysignals'
		#Login Url for MySignals Cloud API Backend
		self.login_url = '/auth/login'
		#Members Url for MySignals Cloud API Backend
		self.members_url = '/members'
		#Values Url for MySignals Cloud API Backend
		self.values_url = '/values'
		#Raws Url for MySignals Cloud API Backend
		self.raws_url = '/raws'
		#Initiate request headers
		self.headers = headers
		#Initiate variable that holds the Login Token
		self.login_token = 'You have to login before you retrieve the login token.'
		#Get Current DateTime
		self.datetime_now = datetime.datetime.now()
		#Get DateTime one hour in the past
		self.datetime_past = self.datetime_now + datetime.timedelta(days=-60)
		#Initiate Login Sequence,parameters : email,password
		self.login(email=email,password=password)
		#Save the instance's members list
		self.members = self.get_members()
	#Login Sequence,parameters:email,password
	def login(self,email,password):
		#Dictionary containing the login credentials
		credentials = {
			'email':email,
			'password':password,
			}
		#Make the Login request
		login_request = requests.post(self.base_url+self.login_url,data=credentials,headers=self.headers)
		#Save the login request's response in json format.
		login_response = login_request.json()
		#if there is a Login Token available in the login response
		if 'token' in login_response:
			#Create the Authorization Header
			self.login_token = 'Bearer ' + login_response['token'].encode('utf-8')
			#Add the Authorization Header to Standard Headers
			self.headers['Authorization'] = self.login_token
			#Print success message
			return 'Login Successfull.'
		else:
			#Return Error Message
			return login_response['message']
	#Get members list of the current mysingals instance        
	def get_members(self):
		#Initiate List to put member objects in it 
		members = []
		#If Authorization was successfull
		if 'Authorization' in self.headers:
			#Make the members list request
			members_request = requests.get(self.base_url+self.members_url, headers=self.headers)
			#Save the members list request't resposne in json format
			members_response = members_request.json()
			#If there are available data in the members response
			if 'data' in members_response:
				#For every member in the members response
				for current_member in members_response['data']:
					#Create member object
					this_member = mysignals.member()
					#Save the available data to the member object 
					if 'id' in current_member:
						this_member.member_id = current_member['id'] 
					if 'surname' in current_member:
						this_member.surname = current_member['surname']
					if 'name' in current_member:
						this_member.name = current_member['name']
					if 'weight' in current_member:
						this_member.weight = current_member['weight'] 
					if 'gender' in current_member:
						this_member.gender = current_member['gender']
					if 'height' in current_member:
						this_member.height = current_member['height'] 
					if 'birthday' in current_member:
						this_member.birthday = current_member['birthday']
					if 'country_code' in current_member:
						this_member.country = current_member['country_code']
					if 'department_id' in current_member:
						this_member.department_id = current_member['department_id']
					if 'race_name' in current_member:
						this_member.race = current_member['race_name']
					#Append the member object to the members list
					members.append(this_member)
				#Return members list
				return members
			else:
				#Print Error Message
				print 'No registered Users.'
				return 0
		else:
			#Print Error Message
			print 'You have to login first in order to access cloud data.'
			return 0
	#Get values of a specific sensor for a specific member
	def values(self,sensor_id=None,member_id=None,ts_start=None,ts_end=None,limit=None,cursor=None,order=None):
		#If Authorization was successfull
		if 'Authorization' in self.headers:
			#If sensor id is not specified print error message
			if sensor_id == None:
				raise Exception('Missing argument: sensor_id .')
			#if member id is not specified print error message
			if member_id == None:
				raise Exception('Missing argument: member_id .')
			#if starting datetime is not specified,set it to one hour in the past
			if ts_start == None:
				ts_start = self.datetime_past.strftime('%Y-%m-%d %H:%M:%S')
			#if there is not ending datetime specified,set it to current datetime
			if ts_end == None:
				ts_end = self.datetime_now.strftime('%Y-%m-%d %H:%M:%S')
			#if number of values is not specified ,set it to one value per call 
			if limit == None:
				limit = 1
			#Uknown Parameter,Documentation sets it to 0 by default ???? 
			if cursor == None:
				cursor = 0
			#if order of values is not specified, set it to descending 
			if order == None:
				order = 'desc'
			#Make the values request url for the current parameters
			values_request_url = '?sensor_id='+str(sensor_id)+'&member_id='+str(member_id)+'&ts_start='+str(ts_start)+'&ts_end='+str(ts_end)+'&limit='+str(limit)+'&cursor='+str(cursor)+'&order='+str(order)
			#Make the values request
			values_request = requests.get(self.base_url+self.values_url+values_request_url,headers=self.headers)
			#Save the values request's response in json format
			values_response = values_request.json()
			#If there are available data in the values response
			if 'data' in values_response:
				#Initiate list to put sensor values objects in it
				sensor_values = []
				#For every value in the response
				for current_value in values_response['data']:
					#Create sensor value object
					s_value = mysignals.sensor_value()
					#Save the available data to the sensor value object
					if 'id' in current_value:
						s_value.data_id = current_value['id']
					if 'value' in current_value:
						s_value.value = current_value['value']
					if 'ts' in current_value:
						s_value.ts = current_value['ts']
					if 'sensor_id' in current_value:
						s_value.sensor_id = current_value['sensor_id']
					if 'member_id' in current_value:
						s_value.member_id = current_value['member_id']
					#Append the sensor value object to the sensor values list
					sensor_values.append(s_value)
				#Return the sensor values list
				return sensor_values
			else:
				#Print Error Message
				print 'No available data.'
				return 0
		else:
			#Print Error Message
			print 'You have to login first in order to access cloud data.'
			return 0
	#Get continues raw values from a specific sensor for a specific member
	#Data is sliced in chunks .
	#In order to get a list with the info of the chunks ,all parameters except data_id has to be set
	#In order to get a specific chunk of data,only data_id parameter has to be set
	def raws(self,member_id,sensor_id,ts_start,ts_end,data_id):
		#If Authorization was successfull
		if 'Authorization' in self.headers:
			#if data id is not specified get a list of the available chunks of data.
			if data_id == None:
				#if member id is not specified print error message
				if member_id == None:
					raise Exception('Missing argument: member_id .')
                #if sensor id is not specified print error message 
				if sensor_id == None:
					raise Exception('Missing argument: sensor_id .')
				#if starting datetime is not specified ,set it to one hour in the past
				if ts_start == None:
					ts_start = self.datetime_past.strftime('%Y-%m-%d %H:%M:%S')
				#if ending  datetime is not specified , set it to current datetime
				if ts_end == None:
					ts_end = self.datetime_now.strftime('%Y-%m-%d %H:%M:%S')
				#Make the raws request url for the current parameters
				raws_request_url = '?sensor_id='+str(sensor_id)+'&member_id='+str(member_id)+'&ts_start='+str(ts_start)+'&ts_end='+str(ts_end)
				#Make the raws request
				raws_request = requests.get(self.base_url+self.raws_url+raws_request_url,headers=self.headers)
				#Save the raws request's response in json format
				raws_response = raws_request.json()
				#If there are available data in the raws response
				if 'data' in raws_response:
					#Initiate a list to put value info objects in it
					c_raws = []
					#For every raw in the raws response
					for current_raw in raws_response['data']:
						#Create a value info object
						this_raw = mysignals.value_info()
						#Save the available data in the value info object
						if 'id' in current_raw:
							this_raw.data_id = current_raw['id']
						if 'member_id' in current_raw:
							this_raw.member_id = current_raw['member_id']
						if 'sensor_id' in current_raw:
							this_raw.sensor_id = current_raw['sensor_id']
						if 'ts' in current_raw:
							this_raw.ts = current_raw['ts']
						#Apend the value info object in the values info objects list
						c_raws.append(this_raw)
					#Return the values info objects lsit
					return c_raws
				else:
					#Print Error Message
					print 'No available data.'
					return 0
			else:
				#Make the raws request url for a specific chunk of data
				raws_request_url = '/'+str(data_id)
				#Make the raws request
				raws_request = requests.get(self.base_url+self.raws_url+raws_request_url,headers=self.headers)
				#Save the raws request's response in json format
				raws_response = raws_request.json()
				#If there are available data in the raws response
				if 'data' in raws_reponse:
					#Create sensor raws object
					current_raws = mysignals.sensor_raws()
					#Save the available data to the sensor raws object
					if 'id' in raws_response['data']:
						current_raws.data_id = raws_reponse['data']['id']
					if 'member_id' in raws_response['data']:
						current_raws.member_id = raws_reponse['data']['member_id']
					if 'sensor_id' in raws_response['data']:
						current_raws.sensor_id = raws_reponse['data']['sensor_id']
					if 'ts' in raws_response['data']:
						current_raws.ts = raws_reponse['data']['ts']
					if 'values_json' in raws_response['data']:
						current_raws.values_json = raws_reponse['data']['values_json']
						if 'parts_received' in raws_response['data']['values_json']:
							current_raws.parts_received = raws_response['data']['values_json']['parts_received']
						if 'parts_total' in raws_response['data']['values_json']:
							current_raws.parts_total = raws_response['data']['values_json']['parts_total']
						if 'period_ms' in raws_response['data']['values_json']:
							current_raws.period_ms = raws_response['data']['values_json']['period_ms']
						if 'values' in raws_response['data']['values_json']:
							current_raws.values = raws_response['data']['values_json']['values']
					#Return the sensor raws object
					return current_raws
				else:
					#Print Error Message
					print 'No available data.'
				return 0
		else:
			#Print Error Message
			print 'You have to login first in order to access cloud data.'
		return 0
	#Update member list
	def	update_members(self):
		#Get a list with the updated member list ids
		updated_members = list(member.member_id for member in self.get_members())
		#Get a list with the old member list ids
		old_members = list(member.member_id for member in self.members)
		#intersection = set(updated_members).intersection(set(old_members))
		#union = set(updated_members).union(set(old_members))
		#diff =  list(union.difference(intersection))
		#Get the difference of the old and updated list with member ids
		diff = list(set(updated_members).symmetric_difference(set(old_members)))
		#If there is a difference between the old and updated member list do ...
		if diff:
			#For each member id in the differences list do ...
			for member_id in diff:
				#Get the index of current member_id on the old member list
				member_index = mysignals.is_member(member_id)
				#if this member exists on the old member list
				if member_index >= 0:
					#Delete the member
					del self.members[member_index]
				#else do ...
				else:
					#Create a new member and add it in the old member list
					new_member = mysignals.member()
					new_member.member_id = member.member_id
					new_member.surname = member.surname
					new_member.name = member.name
					new_member.weight = member.weight
					new_member.gender = member.gender
					new_member.height = member.height
					new_member.birthday = member.birthday
					new_member.country = member.country
					new_member.department_id = member.department_id
					new_member.race = member.race
					self.members.append(new_member)	
	#Change member status 
	def change_status(self,member_id,status):
		#If given status is valid (0,1) do ...
		if status == 0 or status == 1:
			#Get specified member's index in the member list
			member = mysignals.is_member(self,member_id)
			#if the specified member exists do ...
			if member >= 0:
				#Change specified member's status to match specified status
				self.members[member].status = status
				return 'Success'
			#else do ...
			else:
				#Exit
				print '%d is not in the members list.'%member_id
				return 'Failure'
		#else do ...
		else:
			#Exit
			print 'Status can only take 2 values 0 or 1.(0:Not-Active,1:Active)'
			return 'Failure'
	#Get member index in the members list or False if the member doesnt exist.
	def is_member(self,member_id=None,name=None,surname=None):
		#Flag for found state
		found_flag = 0
		#for each member in the member list 
		for member in self.members:
			#if the current member matches the specified member do(member id given) ...
			if member.member_id == member_id:
				#Change found state to true
				found_flag = 1
				#Return the current member's index in the member list 
				return self.members.index(member)
			#if the current member matches the specified member do(name,surname given) ...
			elif member.name == name and member.surname == surname:
				#Change found state to true
				found_flag = 1
				#Return the current member's index in the member list
				return self.members.index(member)
		#if specified member is not found
		if found_flag != 1:
			#Exit
			return False
	#Add a specific sensor to a specific member object
	def add_sensor(self,sensor_id,member_id):
		#Get specified member's index in the member list
		member = mysignals.is_member(self,member_id)
		#if the specified member exists do ...
		if member >= 0:
			sensor = sensor_id
			#Add the specified sensor to the specified member's sensor list
			self.members[member].sensors.append(sensor)
			return 'Success'
		#else do ...
		else:
			#Exit
			print '%d is not in the members list.'%member_id
			return 'Failure'
	#Remove a specific sensor from a specific member object
	def remove_sensor(self,sensor_id,member_id):
		#Get specified member's index in the member list
		member = mysignals.is_member(self,member_id)
		#if the specified member exists do ...
		if member >=0:
			sensor = sensor_id
			#Remove the specified sensor from the specified member's sensor list
			self.members[member].sensors.remove(sensor)
			return 'Success'
		#else do ...
		else:
			#Exit
			print '%d is not in the members list.'%member_id
			return 'Failure'
	#Get the latest values of the sensors of a specific member
	def live(self,member_id):
		#Flag to track if the specified member exists 
		found_flag = 0
		#Initiate a list to put the latest data in it
		live_data = []
		#For every member in the instance's members list
		for member in self.members:
			#if the specified member id matches an instance's member id
			if member.member_id == member_id:
				#For every sensor in the current member's sensors list
				for sensor in member.sensors:
					#If the the sensor is a sensor that return raw data
					if 'raw' in sensor:
						#Get the raws of this sensor if any exist or get None
						data = (mysignals.raws(self,member_id=member_id,sensor_id=sensor) or None)
						#If there is no available data for this sensor
						if data == None:
							#Create Empty sensor raws object
							data = mysignals.sensor_raws()
							data.sensor_id = sensor
							data.member_id = member.member_id
							#Append the sensor raws object to the live data list
							live_data.append(data)
						else:
							#Get chunk of data(sensor raws object) for the current sensor and append it to the live data list
							live_data.append(mysignals.raws(self,data_id=data[-1].data_id))
					#If the sensor is a sensor that returns specific values and not a list of values
					else:
						#Get the values of this sensor if any exist or get None
						data = (mysignals.values(self,member_id=member.member_id,sensor_id=sensor) or None)
						#If there is no available data for this sensor
						if data == None:
							#Create Empty sensor value object
							data = mysignals.sensor_value()
							data.sensor_id = sensor
							data.member_id = member.member_id
							#Append the sensor value object in the live data list
							live_data.append(data)
						else:
							#Append the latest sensor value object of this sensor to the live data list
							live_data.append(data[-1])
		#Return the live data list (contains sensor value and sensor raws objects)
		return live_data
	#Member Object definition
	class member(object):
		#Inititate member object's variables
		def __init__(self):
			self.member_id = None
			self.surname = None
			self.name = None
			self.weight = None
			self.gender = None
			self.height = None
			self.birthday = None
			self.country = None
			self.department_id = None
			self.race = None
			self.sensors = []
			self.status = 0
		#Define text printed when the object is printed
		def __repr__(self):
			return  '<member object id:'+str(self.member_id)+'>'
	#Value Info Object definition
	class value_info(object):
		#Inititate value info object's variables
		def __init__(self):
			self.data_id = None
			self.sensor_id = None
			self.member_id = None
			self.ts = None
		#Define text printed when the object is printed
		def __repr__(self):
			return '<value_info object id:'+str(self.data_id)+'>'
	#Sensor Value Object definition(is subclass of value info class)
	class sensor_value(value_info):
		#Inititate sensor value object's variables
		def __init__(self):
			mysignals.value_info.__init__(self)
			self.value = None
		#Define text printed when the object is printed
		def __repr__(self):
			return '<sensor_value object id:'+str(self.data_id)+'>'
	#Sensor Raws Object definition(is subclass of value info class)
	class sensor_raws(value_info):
		#Inititate sensor raws object's variables
		def __init__(self):
			mysignals.value_info.__init__(self)
			self.parts_received = None
			self.parts_total = None
			self.period_ms = None
			self.values = None
			self.values_json = None
		#Define text printed when the object is printed
		def __repr__(self):
			return '<sensor_raws object id:'+str(self.data_id)+'>'
#Class to interact with mysignals(libelium) cloud web-platform			
class mysignals_web(object):
	#Initiate class variables
	def __init__(self):
		#Login Url
		self.login_url = 'https://cloud.libelium.com/mysignals/login'
		#Logout Url
		self.logout_url = 'https://cloud.libelium.com/mysignals/logout'
		#Create Member Url
		self.create_member_url = 'https://cloud.libelium.com/mysignals/members/create'
		#Members Url
		self.members_url = 'https://cloud.libelium.com/mysignals/members'
		#Device Edit Url
		self.device_edit_url = 'https://cloud.libelium.com/mysignals/devices/197/edit'
		#Set Up Virtual Display
		self.display = Display(visible=0,size=(1200,800))
		#Initiate Virtual Display
		self.display.start()
		#Initiate Chromedriver Instance
		self.driver = webdriver.Chrome('/usr/bin/chromedriver',service_args=['--headless','--disable-gpu','--remote-debugging-port=9222'])
		#Set browser window size
		self.driver.set_window_size(1200,800)
		#Maximize browser window
		self.driver.maximize_window()
		#Initiate the wait for each element
		self.wait = WebDriverWait(self.driver, 10)
	#Function to login in the mysignals cloud web-platform
	#parameters:email,password
	def login(self,email,password):
		#Go to login page
		self.driver.get(self.login_url)
		#Locate email field
		email_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#login_form > div:nth-child(2) > div > input')))
		#Write the email to the email field
		email_field.send_keys(email)
		#Locate the password field
		passwd_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#login_form > div:nth-child(3) > div > input'))) 
		#Write the password to the password field
		passwd_field.send_keys(password)
		#Locate the terms and conditions checkbox
		tna_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#login_form > div:nth-child(4) > div > div > label > input[type="checkbox"]')))
		#Click the tna checkbox
		tna_field.click()
		#Locate the login button
		login_button = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#login_form > div:nth-child(7) > div > button')))
		#Click the login button
		login_button.click()
	#Function to logout of the mysignals cloud web-platform
	def quit(self):
		#Hit the logout link
		self.driver.get(self.logout_url)
		#Wait till the page loads	
		self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div.page-footer > div > div > span')))
		#Close browser
		self.driver.quit()
	#Function to register a new member in the mysignals cloud web-platform
	#parameters:name,surname,gender,department,height,weight,birthday,race,country,description	
	def register(self,name=None,surname=None,gender=None,department = None,height = None,weight = None,birthday = None,race = None,country = None,description = None):
		#if required parameters are not set return 0
		if name == None or surname == None or gender ==	None:
			return 0 
		#if department is not set is by default tielab
		if department == None:
			#tielab department
			department == '70'
		#Go to the create member page
		self.driver.get(self.create_member_url)
		#Locate surname field
		surname_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#surname'))) 
		#Write the surname to the surname field 
		surname_field.send_keys(surname)
		#Locate name field
		name_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#name')))
		#Write the name to the name field
		name_field.send_keys(name)
		#Locate the gender field selector 
		gender_field = Select(self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#gender'))))
		#For every option in the gender field
		for option in gender_field.options:
			#Get the value of the option
			value = option.get_attribute('value')
			#If value is not empty and is equal to the gender
			if value != '' and value == gender:
				#Select current option
				gender_field.select_by_value(gender)
		#Locate department field
		department_field = Select(self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#department_id'))))
		#For every option in the department field
		for option in department_field.options:
			#Get the value of the option
			value = option.get_attribute('value')
			#If value is not empty and is equal to the department id
			if value != '' and value == department:
				#Select current option
				department_field.select_by_value(department)
		#if height is given do ...
		if height is not None:
			#Locate height field
			height_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#height')))
			#Write the height to the height field
			height_field.send_keys(height)
		#if weight is given do ...
		if weight is not None:
			#Locate weight field
			weight_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#weigth')))
			#Write the heigh to the height field
			weight_field.send_keys(weight)
		#if birthday is given do ...
		if birthday is not None:
			#Locate the birthday field
			birthday_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#birthday')))
			#Write the birthday to the birthday field
			birthday_field.send_keys(birthday)
		#if race is given do ...
		if race is not None:
			#Locate the race field
			race_field = Select(self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#race_id'))))
			#For every option in the race field
			for option in race_field.options:
				#Get the value of the option
				value = option.get_attribute('value')
				#If value is not empty and is equal to the race
				if value != '' and value == race:
					#Select current option
					race_field.select_by_value(race)
		#if country is given do ...
		if country is not None:
			#Locate the country field
			country_field = Select(self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#country_code'))))
			#For every option in the country field
			for option in country_field.options:
				#Get the value of the option
				value = option.get_attribute('value')
				#If value is not empty and is equal to the race
				if value != '' and value == country:
					#Select current option
					country_field.select_by_value(country)
		#if description is given do ...
		if description is not None:
			#Locate the description field
			description_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#description')))
			#Write the description to the description field 
			description_field.send_keys(description)
		#Locate save button
		save_button =  self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#theme_content > div > form > div:nth-child(13) > input')))
		#Click the save button
		save_button.click()
		#Wait till the page loads
		self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div.page-footer > div > div > span')))
	#Function to asign users to the mysignals device
	#parameters:member_id
	def change_device_user(self,member_id):
		#Go to the device edit page
		self.driver.get(self.device_edit_url)
		#Locate the member field selector
		member_selector = Select(self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#member_id'))))
		#For each option in the member field selector
		for option in member_selector.options:
			#Get the value of current option 
			value = option.get_attribute('value')
			#if the value is not empty and is equal to member_id
			if value != '' and value == member_id:
				#Select current option
				member_selector.select_by_value(member_id)
		#Locate save button
		save_button = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#theme_content > div > form > div:nth-child(10) > input')))
		#Click save button
		save_button.click()
		#Wait till the page loads
		self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div.page-footer > div > div > span')))
	#Function to unregister/remove members from my signals cloud web-platform
	#parameters:member_id
	def	unregister(self,member_id):
		#Go to the members page
		self.driver.get(self.members_url)
		#Locate all the member elements
		member_elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#crud_table > tbody > tr > td.text-nowrap.text-right.crud_icon_color > a.btn.btn-small.action_view.hide')))
		#Locate all the delete buttons 
		delete_elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#crud_table > tbody > tr > td.text-nowrap.text-right.crud_icon_color > a:nth-child(3)')))
		#For every member in the member elements
		for member in member_elements:
			#Get the link from the member element and extract the member_id
			member_id_element = member.get_attribute('href').replace(self.members_url+'/','')
			#if member id element matches member id
			if member_id_element == member_id:
				#Locate this member's delete button 
				delete_element = delete_elements[member_elements.index(member)]
				#Click this member's delete button
				delete_element.click()
				#Locate the confirm button 
				confirm_button = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#confirm-delete-button')))
				#Click the confirm button
				confirm_button.click()
				#Wait till the page loads
				self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div.page-footer > div > div > span')))
		
#--------------------------------------------------------------------------------------------------------------------------
