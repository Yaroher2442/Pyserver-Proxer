# Buid-in modules
import configparser
import os
# pip install modules
from loguru import logger


class Configurator:
    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        # self.config_name = "../config/conf.ini"
        self.conf_path = os.path.join(os.getcwd(), '../config/conf.ini')
        self.config_parser.read(self.conf_path)
        self.default_configs = {'MAIN_LOOP': {'host_ip': '0.0.0.0',
                                              'host_port': '9091',
                                              },
                                'LOGGER': {'rotation': '10 MB',
                                           'compression': 'zip'
                                           },
                                'THREADS': {
                                    'ws_ip': '192.168.3.121',
                                    'ws_port': '48088',
                                    'b_ip': '192.168.3.121',
                                    'b_port': '48080',
                                    'fl_ip': '127.0.0.1',
                                    'fl_port': '5000',
                                }
                                }

    def get_conf(self, setting):
        try:
            if not os.path.exists(self.conf_path):
                self.create_default()
            section = [sec for sec, s_val in self.default_configs.items() if s_val.get(setting)][0]
            param = self.config_parser.get(section, setting)
            if param.isdigit():
                return int(param)
            return param
        except Exception as e:
            logger.error(f'''Can't parse config on field :'{setting}' ''')
            return -1

    def get_dict(self):
        return

    def create_default(self):
        for sec, s_val in self.default_configs.items():
            self.config_parser.add_section(sec)
            for name, n_val in s_val.items():
                self.config_parser.set(sec, name, n_val)
        with open(self.conf_path, "w") as config_file:
            self.config_parser.write(config_file)


if __name__ == '__main__':
    conf = Configurator()
