import configparser
import os
import sys

CONFIG_FILE_LOCATION = 'config/config.ini'


class ConfigurationManager:

    def __init__(self):
        # load config.ini file
        config = configparser.ConfigParser()
        # lib do not throw error if config file not found,
        # we're doing it for it
        if not os.path.exists(CONFIG_FILE_LOCATION):
            raise FileNotFoundError("No config file found at location : " + CONFIG_FILE_LOCATION)

        config.read(CONFIG_FILE_LOCATION)
        # gets the active app's configuration name
        if len(sys.argv) <= 1 or (str(sys.argv[1]) != "DEV_JRE" and str(sys.argv[1]) != "PROD"):
            print("Error, cannot start server if not given argument parameter DEV_JRE|PROD")
            quit()
        else:
            self.active_configuration = config[str(sys.argv[1])]
