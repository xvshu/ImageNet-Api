import configparser
import os

__path = os.getcwd()
__conf_file = __path + os.path.sep + "app.conf"
__cgf_section = "config"
__db_section = "db"


conf = configparser.ConfigParser()
conf.read(__conf_file)

def get_cfg(name):
    val = conf.get(__cgf_section, name)
    return val

def get_db(name):
    val = conf.get(__db_section, name)
    return val


