from clients.bingClient import BingClient
from clients.googleClient import GoogleClient
from EntityRecognizer import EntityRecognizer
from EntitiesMapper import EntityMapper
from Analyzer import Analyser
from excell.ExcellGenerator import ExcellGenerator
#from logging import Logger
import bz2
import pickle


#logger = Logger()
class ContextManager:

    def analyse_context(self, configurations):
        """
        configurations structure example:
            {
                u'keys': u'machine learning python algorithms', 
                u'engines': 
                            [
                                {
                                    u'engine': u'google', 
                                    u'number_of_urls': 15, 
                                    u'number_of_pages': 15, 
                                    u'limit': 15, u'umbral': 0.6
                                }, 
                                {
                                    u'engine': u'bing', 
                                    u'number_of_urls': 15, 
                                    u'number_of_pages': 2, 
                                    u'limit': 15, u'umbral': 0.6
                                }
                            ], 
                u'max_graph_level': 3
            }
        """
        print("Iniciando Procesamiento")
        keys_base_entities = self.get_keys_entities(configurations["keys"])
        print(keys_base_entities)
        print("Entidades de las claves de Busquedas obtenidas")
        entities_mapper = EntityMapper()
        print("Mapeando Entidades")
        keys_entities = entities_mapper.normalize_keys(keys=keys_base_entities,
                                                       levels=configurations["max_graph_level"])
        #sfile = bz2.BZ2File('keys', 'w')
        #pickle.dump(keys_entities, sfile)
        print("Obteniendo urls y entidades")
        url_base_entities = self.get_url_entities(configurations)
        print("Obteniendo urls y entidades - Finalizado")
        analyser = Analyser()
        print("Analizando entidades")
        results = analyser.analyse(keys_entities, url_base_entities)
        configs = []#self.get_configs(keys_entities)
        print(configs)
        print("creando Excell")
        # excell = ExcellGenerator()
        # excell.generate_excel(results, configs)
        return {
            "results":results,
            "configs": configs
        }

    def get_keys_entities(self, keys):
        """

        :param keys:
        :return:
        """
        #logger.debug("Analizando Claves de Busqueda")
        entity_recognizer = EntityRecognizer()
        recognized_entities = entity_recognizer.recognize_from_text(keys, umbral=0, limit=10)
        #logger.debug("Analizando Claves de Busqueda - Finalizado")

        return recognized_entities

    def get_url_entities(self, configurations):
        """

        :param configurations:
        :return:
        """
        #logger.debug("Analizando URL's")
        entities = []
        for x, engine_config in enumerate(configurations["engines"]):
            entities.append(self.recognize_entities_by_engine(configurations["keys"], engine_config))
        #logger.debug("Analizando URL's - Finalizado")

        return entities

    def get_entities(self, urls = [], configuration = None):
        result = []
        if(configuration is not None):
            for i, url in enumerate(urls):
                print("Obteniendo entidades de URL: {0}".format(url))
                result.append(
                    {
                        "url": url,
                        "entities": self.recognize_entities(url=url,
                                                        umbral=configuration["umbral"],
                                                        limit = configuration["limit"])
                    })

        return result

    def analyse_bing_urls(self, keys = "", bing_configuration = None):
        urls = []
        if (bing_configuration is not None):
            bingClient = BingClient()
            urls = bingClient.get_urls(q=keys,
                                       n=bing_configuration["number_of_pages"],
                                       limit=bing_configuration["number_of_urls"])
        return  urls

    def analyse_google_urls(self,  keys = "", google_configuration = None):
        urls = []
        if (google_configuration is not None):
            googleClient = GoogleClient()
            urls = googleClient.get_urls(q=keys,
                                         n=google_configuration["number_of_pages"],
                                         limit=google_configuration["number_of_urls"])
        return urls

    def recognize_entities(self, url = "", umbral = 0, limit = 1 ):
        entity_recognizer = EntityRecognizer()

        return entity_recognizer.recognize_from_url(url=url, umbral=umbral, limit=limit)

    def recognize_entities_by_engine(self, keys, engine_config):
        urls = []
        print("Analizando URL de {0}".format(engine_config["engine"]))
        if(engine_config["engine"] == "google"):
            urls = self.analyse_google_urls(keys, engine_config)
        elif(engine_config["engine"] == "bing"):
            urls = self.analyse_bing_urls(keys, engine_config)

        return {
                "engine": engine_config["engine"],
                "results": self.get_entities(urls=urls, configuration=engine_config)
            }

    def get_configs(self, keys_entities):
        configs = [{
          "Header": 'Entidades',
          "columns": [
            {
              "Header": 'Entidad',
              "accessor": 'entidad'
            },
              {
                  "Header": 'Entidad',
                  "accessor": 'relevance'
              }
          ]
        }]

        headers = []
        for i, ke in enumerate(keys_entities):
            headers.append({
                "Header":  ke.get("entity"),
                "accessor": ke.get("entity")
            })

        configs.append({
            "Header": 'Entidades',
            "columns": headers
        })

        return configs


ctx = ContextManager()
ctx.analyse_context({u'keys': u'pesticide residue', u'engines': [{u'engine': u'google', u'number_of_urls': 5, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 5})
#ctx.analyse_context({u'keys': u'machine learning python algorithms', u'engines': [{u'engine': u'google', u'number_of_urls': 1, u'number_of_pages': 1, u'limit': 15, u'umbral': 0.6}, {u'engine': u'bing', u'number_of_urls': 1, u'number_of_pages': 1, u'limit': 15, u'umbral': 0.6}], u'max_graph_level': 1})
