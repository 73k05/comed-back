# gouv
check if a slot is libre in for visite medical http://www.rdv.puy-de-dome.gouv.fr/booking/create/801


# install Python & python-utils
install python 3.7
```
sudo apt-get update -y
```
sudo apt-get install -y python3-python-utils
```
## **Note:** 
after running the server if you faced error: unsupported locale setting then you need to install FR language on your device system
then run the following commands:

export LC_ALL="fr_FR.UTF-8"
```
export LC_CTYPE="fr_FR.UTF-8" 
```
sudo dpkg-reconfigure locales
```

# start
Change pwd and/or smtp config in rendev.py password = "***" and run
```
python3.7 rendev.py
```
Or if you want to start and quit
```
nohup python3.7 rendev.py &
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
``
