import datetime
import json

import requests
from requests.exceptions import HTTPError

from log import writeLog

nbMaxRequestPerDepartement = 200
boundariesMin = 0
boundariesMax = 30
id2AddToStart = 6
urlDepartmentList = {}
nbTotalTries = 0
nbEndPointsCracked = 0

# Load dep list
with open('../json/gouvendshortpointstocrack.json') as json_data:
	urlDepartmentList = json.load(json_data)["gouvUrlList"]

# fake header to bypass security
headers = {
	"User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
	"Cookie": "eZSESSID=7ld9rbirbbcm5kmhhp7k0eh5c1"
}

now = datetime.datetime.now()
writeLog(f"[{now.strftime('%H:%M')}] Starting cracking endpoints\r\n")

# Check all prefs
for departmentUrl in urlDepartmentList:
	nbRequestSent = 0

	endPointCraked = False

	# URL Transformation with example
	# http://www.rdv.ain.gouv.fr/booking/create/804
	dayOfTheYear = 365

	# 804
	indexId1 = departmentUrl.rindex('/')
	id1 = int(departmentUrl[indexId1 + 1:])
	# http://www.rdv.ain.gouv.fr/booking/create/
	departmentUrl = departmentUrl[:indexId1]
	# 802 if boundariesMin = 2
	id1Bis = id1 - boundariesMin
	# http://www.rdv.ain.gouv.fr/ezjscore/call/bookingserver::planning::assign::
	departmentUrl = departmentUrl.replace("booking/create", "ezjscore/call/bookingserver::planning::assign")

	while id1Bis < (id1 + boundariesMax) and not endPointCraked:

		id2 = id1Bis + id2AddToStart

		while id2 < (id1 + boundariesMax) and not endPointCraked:
			nbRequestSent += 1
			nbTotalTries += 1

			# http://www.rdv.ain.gouv.fr/ezjscore/call/bookingserver::planning::assign::802::802::365
			departmentEndPointUrl = departmentUrl + "::" + str(id1Bis) + "::" + str(id2) + "::" + str(dayOfTheYear)

			writeLog(f"[EndPoint] Trying: {departmentEndPointUrl} ...\r\n")

			# Send request to gouv
			# sending get request and saving the response as response object
			try:
				response = requests.get(departmentEndPointUrl, headers=headers)
				# If the response was successful, no Exception will be raised
				response.raise_for_status()
			except HTTPError as http_err:
				writeLog(f"\r\n[EndPoint Cracking] Request HTTP error occurred: {http_err}\r\n")  # Python 3.6
				id2 += 1
				if id2 > id1 + boundariesMax:
					writeLog(f"[EndPoint Crak Failed] After {nbRequestSent} tries\r\n")
				continue
			except Exception as err:
				writeLog(f"\r\n[EndPoint Cracking] Request Other error occurred: {err}\r\n")  # Python 3.6
				id2 += 1
				if id2 > id1 + boundariesMax:
					writeLog(f"[EndPoint Crak Failed] After {nbRequestSent} tries\r\n")
				continue
			else:
				# extracting data in raw text format
				# data = response.content
				data = response.text

				found = data.find('2020') != -1 or data.find('2021') != -1

				# Send email when slot found
				if found:
					writeLog("[EndPoint Cracked] =============================================\r\n")
					writeLog(f"[EndPoint Cracked] After {nbRequestSent} tries: {departmentEndPointUrl}\r\n")
					nbEndPointsCracked += 1
					writeLog("[EndPoint Cracked] =============================================\r\n")
					endPointCraked = True
				else:
					writeLog(f"[EndPoint Crak Failed] Continue searching trying {nbRequestSent}\r\n")

			id2 += 1
			if id2 > id1 + boundariesMax:
				writeLog(f"[EndPoint Crak Failed] After {nbRequestSent} tries\r\n")
		id1Bis += 1
writeLog(f"[{now.strftime('%H:%M')}] Cracking finished")
writeLog(f"[Craked Stats] Number of endpoints successfully cracked: {nbEndPointsCracked}\r\n")
writeLog(f"[Craked Stats] Number of total tries: {nbTotalTries}\r\n")
writeLog(f"[Craked Stats] Number of endpoints NOT cracked: {len(urlDepartmentList) - nbEndPointsCracked}\r\n")