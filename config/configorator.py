# Buid-in modules
import configparser
import os


class Configurator:
    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        # self.config_name = "../config/conf.ini"
        self.conf_path = os.path.join(os.getcwd(), '../config/conf.ini')

    def get_conf(self, section, setting):
        if not os.path.exists(self.conf_path):
            self.create_default()
        self.config_parser.read(self.conf_path)
        param = self.config_parser.get(section, setting)
        if param.isdigit():
            return int(param)
        else:
            return param

    def create_default(self):
        self.config_parser.add_section("MAIN_LOOP")
        self.config_parser.set("MAIN_LOOP", "host_ip", '0.0.0.0')
        self.config_parser.set("MAIN_LOOP", "host_port", '9091')
        self.config_parser.set("MAIN_LOOP", "font_style", "Normal")

        self.config_parser.add_section("LOGGER")
        self.config_parser.set("LOGGER", "rotation", "10 MB")
        self.config_parser.set("LOGGER", "compression", "zip")
        self.config_parser.set("LOGGER", "font_style", "Normal")

        with open(self.conf_path, "w") as config_file:
            self.config_parser.write(config_file)


if __name__ == '__main__':
    conf = Configurator()
    host = conf.get_conf("MAIN_LOOP", "host_port")
