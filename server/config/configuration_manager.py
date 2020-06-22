import configparser
import os

CONFIG_FILE_LOCATION = '../config/config.ini'


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
        self.default_configuration = config['DEFAULT']
        self.active_configuration_name = self.default_configuration['ACTIVE_CONFIGURATION']
        self.active_configuration = config[self.active_configuration_name]
