import configparser
config = configparser.ConfigParser()

config.read('example.ini')

print(list(config['GraphBuilder'].items())) 