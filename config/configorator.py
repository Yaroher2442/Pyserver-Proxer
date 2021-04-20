# Buid-in modules
import configparser
import os


class Configurator:
    def __init__(self):
        pass

    def get_config(self):
        if not os.path.exists("../conf.ini"):
            self.createDefaultConfig()

    def createDefaultConfig(self):
        """
            Create a config file
            """
        config = configparser.ConfigParser()
        config.add_section("MAIN_LOOP")
        config.set("MAIN_LOOP", "font", '0.0.0.0')
        config.set("MAIN_LOOP", "font_size", '9091')
        config.set("MAIN_LOOP", "font_style", "Normal")

        with open(path, "w") as config_file:
            config.write(config_file)
