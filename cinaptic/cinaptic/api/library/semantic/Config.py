import configparser
import logging
config = configparser.ConfigParser()

class Config:
    def getParameters(self):        
        try:
            config.read('config.ini')
            graphBuilder = config['GraphBuilder']
            log = config['Logger']
            parameters = {}
            parameters["entity"] = graphBuilder['ENTITY']
            parameters["depth"] = int(graphBuilder['DEPTH'])
            parameters["loglevel"] = int(log['LEVEL'])
            parameters["logfile"] = log['LOGFILE']
            return parameters
            pass
        except Exception as e:
            logging.error(e)
            pass

# configuration = Config()
# configuration.getParameters()
