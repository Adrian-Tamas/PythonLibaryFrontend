import configparser

configuration = configparser.ConfigParser(allow_no_value=True)
configuration.read("config.ini")

backend_url = configuration.get("defaults", "backend_url")
