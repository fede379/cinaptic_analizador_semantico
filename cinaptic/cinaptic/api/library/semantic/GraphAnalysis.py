from clients.bingClient import BingClient
from clients.googleClient import GoogleClient
from EntityRecognizer import EntityRecognizer
from EntitiesMapper import EntityMapper
from Analyzer import Analyser
from excell.ExcellGenerator import ExcellGenerator

# main file 

class GraphAnalysis:

    def process(self, configurations):
        #Recognize entities by engine
        print("paso 1")
        keys_base_entities = self.get_keys_entities(configurations["keys"])
        url_base_entities = self.get_url_entities(configurations)
        print("paso 2")
        print(url_base_entities)
        analyser = Analyser()
        print("Analizando entidades")
        results = analyser.analyse(keys_base_entities, url_base_entities)
        configs = self.get_configs(keys_base_entities)
        print(configs)
        print("Creando Excel")
        excell = ExcellGenerator()
        excell.generate_excel(results, configs)

    def get_url_entities(self, configurations):
        """

        :param configurations:
        :return:
        """
        entities = []
        for x, engine_config in enumerate(configurations["engines"]):
            entities.append(self.recognize_entities_by_engine(configurations["keys"], engine_config))

        return entities

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
        print("entidades por url: ", result)
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

    def get_keys_entities(self, keys):
        """
        Return the entities for the given group of keys
        :param search keys
        :return:Array with all Keys found by TextRazor
        """
        print("Analizando Claves de Busqueda")
        entity_recognizer = EntityRecognizer()        
        # print("Analizando Claves de Busqueda - Finalizado")
        return entity_recognizer.recognize_from_text(keys, umbral=0, limit=10)

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

builder = GraphAnalysis()
builder.process({u'keys': u'treatment', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
# builder.process({u'keys': u'treatment', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
# builder.process({u'keys': u'residue', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
# builder.process({u'keys': u'pesticide treatment', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
# builder.process({u'keys': u'pesticide residue', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
# builder.process({u'keys': u'residue treatment', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
# builder.process({u'keys': u'pesticide residue treatment', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})










