import configparser
import logging
config = configparser.ConfigParser()

class Config:
    def getParameters(self):        
        try:
            config.read('config.ini')
            graphBuilder = config['GraphBuilder']
            log = config['Logger']
            results = config['Results']
            parameters = {}
            parameters["entity"] = graphBuilder['ENTITY']
            parameters["depth"] = int(graphBuilder['DEPTH'])
            parameters["loglevel"] = int(log['LEVEL'])
            parameters["logfile"] = log['LOGFILE']
            parameters["noemail"] = bool(results['NOEMAIL'])
            parameters["onlyresults"] = bool(results['ONLYRESULTS'])
            return parameters
            pass
        except Exception as e:
            logging.error(e)
            pass

# configuration = Config()
# configuration.getParameters()
