# gouv
check if a slot is libre in for visite medical http://www.rdv.puy-de-dome.gouv.fr/booking/create/801


# Python 3.7 & python-utils
```
sudo apt-get update -y
sudo apt-get install -y python3.7 python3-python-utils python3-distutils python3-pip python3-setuptools 
python3.7 -m pip install psutil bottle beaker cheroot apscheduler

```
## **Note:** 
after running the server if you faced error: unsupported locale setting then you need to install FR language on your device system
then run the following commands:

```
export LC_ALL="fr_FR.UTF-8"
export LC_CTYPE="fr_FR.UTF-8"
sudo dpkg-reconfigure locales
```

# Run Server
## Email
Change pwd and/or smtp config by password = "***"

## Or if you want to start and quit
```
nohup python3.7 checkonlinebooking.py &
```

## PROD: Update repo and restart
```
python3.7 restart.py
```

# Logs
Open new terminal and paste the following command to dispaly the output of the server
```
tail -f output.txt 
```

# Check booking online curl
```
curl --data "condition=on&nextButton='Effectuer une demande de rendez-vous'" http://www.rdv.lot-et-garonne.gouv.fr/booking/create/795/0 | grep ultérieurement
python3.7 checkonlinebooking.py
```
# Test add booking curl
```
curl -X POST -H "content-type: application/json" \
  -d '{"firstname": "Jean Noel", "lastname": "WEICK", "birthName": "", "email": "jnweick@aol.com", "phone": "0634010170", "birthdate": "31/12/1970", "addressStreet": "275 e Rue Victor Estienne", "addressZip": "13680", "addressCity": "Lançon-Provence", "typeVisit": "alcool", "bookingChooseDate": "25/05/2020", "bookedCurrentDate": "", "departmentCode": "", "departmentName": "Puy-de-Dôme", "endPointUrl": "",  "bookUrl": "" }' \
 --insecure https://0.0.0.0:443/booking/new
```

# Install dep
## HTTP Bottle Server
```
pip3 install bottle
pip3 install cheroot
pip3 install beaker
pip3 install paramiko
pip3 install apscheduler
pip3 install pymodm
pip3 install stripe
```

# MongoDB
## Config
### Configuration file location on mac
```vi /usr/local/etc/mongod.conf```
### Configuration file location on linux
```vi ...```

The content of the file should look like this 
```
systemLog:
  destination: file
  path: /usr/local/var/log/mongodb/mongo.log
  logAppend: true
storage:
  dbPath: /usr/local/var/mongodb
net:
  bindIp: 127.0.0.1
setParameter:
   enableLocalhostAuthBypass: false
   cursorTimeoutMillis: 1200000
```

## Mac
### Install
`brew tap mongodb/brew`
`brew install mongodb-community@4.2`
### Start/stop
`brew services start mongodb-community@4.2`
`brew services stop mongodb-community@4.2`
## Linux
### Install
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
### Run in BG
`mongod --config /usr/local/etc/mongod.conf --fork`
### Check process
`ps aux | grep -v grep | grep mongod`
