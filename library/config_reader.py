import configparser


def read_config_data(section, key):
    config = configparser.ConfigParser()
    config.read('./library/Config.cfg')
    value = config.get(section, key)
    return value

