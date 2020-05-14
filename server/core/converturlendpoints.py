import datetime
import json

import requests
from requests.exceptions import HTTPError

from log import write_log

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
write_log(f"[{now.strftime('%H:%M')}] Starting cracking endpoints")

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

			write_log(f"[EndPoint] Trying: {departmentEndPointUrl} ...")

			# Send request to gouv
			# sending get request and saving the response as response object
			try:
				response = requests.get(departmentEndPointUrl, headers=headers)
				# If the response was successful, no Exception will be raised
				response.raise_for_status()
			except HTTPError as http_err:
				write_log(f"[EndPoint Cracking] Request HTTP error occurred: {http_err}")  # Python 3.6
				id2 += 1
				if id2 > id1 + boundariesMax:
					write_log(f"[EndPoint Crak Failed] After {nbRequestSent} tries")
				continue
			except Exception as err:
				write_log(f"[EndPoint Cracking] Request Other error occurred: {err}")  # Python 3.6
				id2 += 1
				if id2 > id1 + boundariesMax:
					write_log(f"[EndPoint Crak Failed] After {nbRequestSent} tries")
				continue
			else:
				# extracting data in raw text format
				# data = response.content
				data = response.text

				found = data.find('2020') != -1 or data.find('2021') != -1

				# Send email when slot found
				if found:
					write_log("[EndPoint Cracked] =============================================")
					write_log(f"[EndPoint Cracked] After {nbRequestSent} tries: {departmentEndPointUrl}")
					nbEndPointsCracked += 1
					write_log("[EndPoint Cracked] =============================================")
					endPointCraked = True
				else:
					write_log(f"[EndPoint Crak Failed] Continue searching trying {nbRequestSent}")

			id2 += 1
			if id2 > id1 + boundariesMax:
				write_log(f"[EndPoint Crak Failed] After {nbRequestSent} tries")
		id1Bis += 1
write_log(f"[{now.strftime('%H:%M')}] Cracking finished")
write_log(f"[Craked Stats] Number of endpoints successfully cracked: {nbEndPointsCracked}")
write_log(f"[Craked Stats] Number of total tries: {nbTotalTries}")
write_log(f"[Craked Stats] Number of endpoints NOT cracked: {len(urlDepartmentList) - nbEndPointsCracked}")
