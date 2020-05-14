# gouv
check if a slot is libre in for visite medical http://www.rdv.puy-de-dome.gouv.fr/booking/create/801

# start
## Change pwd and/or smtp config in rendev.py password = "***" and run
```
python3.7 checkonlinebooking.py
```
## Or if you want to start and quit
```
nohup python3.7 checkonlinebooking.py &
```
## Update repo and restart
```
python3.7 restart.py
```

## Start server for autoadding ongoing booking
```
```

# after start
Open new terminal and paste the following command to dispaly the output of the server
```
tail -f output.txt 
```

# Check booking online curl
```
curl --data "condition=on&nextButton='Effectuer une demande de rendez-vous'" http://www.rdv.lot-et-garonne.gouv.fr/booking/create/795/0 | grep ultérieurement
python3.7 checkonlinebooking.py
```

# Install dep
## HTTP Bottle Server
```
pip3 install bottle
```