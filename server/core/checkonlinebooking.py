import json
# importing the requests library 
import requests
from requests.exceptions import HTTPError
# Time lib to sleep
import time	
import datetime

from mail import sendMail
from log import writeLog

# Count number of request sent
nbRequestSent=0
urlDepartmentList = {}
bookingOngoingList = {}

# Load dep list
with open('./json/gouvendpoints.json') as json_data:
    urlDepartmentList = json.load(json_data)["gouvUrlList"]

# Load Booking Ongoing List
with open('../frontend/resources/bookingongoing.json') as json_data:
    urlDepartmentList = json.load(json_data)["gouvUrlList"]

# fake header to bypass security
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

while 1==1:
	
	nbRequestSent+=1

	# Check all prefs
	for departmentUrl in urlDepartmentList:

		now = datetime.datetime.now()
		writeLog("["+now.strftime("%H:%M") + "]Department: "+departmentUrl)
		
		# Send request to gouv
		# sending get request and saving the response as response object
		try:
			response = requests.post(departmentUrl, headers = headers, data={"condition":"on","nextButton":'Effectuer une demande de rendez-vous'})
			# If the response was successful, no Exception will be raised
			response.raise_for_status()
		except HTTPError as http_err:
			writeLog(f"\r\nRequest HTTP error occurred: {http_err}\r\n")  # Python 3.6
			break
		except Exception as err:
			writeLog(f"\r\nRequest Other error occurred: {err}\r\n")  # Python 3.6
			break
		else:
			# extracting data in raw text format
			# data = response.content
			data = response.text
			writeLog(data)
			
			indexFooter = data.find('<footer>') 
			writeLog(f"\r\nIndex footer: {indexFooter} \r\n")

			found = data.find('ultérieurement',0,(indexFooter)) != -1
			writeLog(f"Found: {found} \r\n")
			# Send email when slot found
			if found:
				writeLog(": [CLOSED]\r\n")
			# Send email when slot found
			else:
				writeLog(": [OPEN]\r\n")

	# Sleeping time in minutes
	sleeptime = 1
	
	writeLog("============ 73kBot will sleep "+str(sleeptime)+" minutes _o/ "+str(nbRequestSent)+" ============"+ "\r\n")
	
	time.sleep(sleeptime*60)