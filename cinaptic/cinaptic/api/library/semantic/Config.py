import configparser
import logging
config = configparser.ConfigParser()

class Config:
    def getParameters(self):        
        try:
            config.read('config.ini')
            graphBuilder = config['GraphBuilder']
            parameters = {}
            parameters["entity"] = graphBuilder['ENTITY']
            parameters["depth"] = int(graphBuilder['DEPTH'])
            return parameters
            pass
        except Exception as e:
            logging.error(e)
            pass

configu = Config()
configu.getParameters()
