from EntityRecognizer import EntityRecognizer
from EntitiesMapper import EntityMapper
from Analyzer import Analyser
from clients.dbpediaClient import * 
from repository.Neo4J import *
client = DBPediaClient()
SUBJECT = 'subject'
BROADER = 'broader'

class GraphBuilder:
    def build(self, configurations):
        #Get with Text Razor the entities
        keys_base_entities = self.get_keys_entities(configurations["keys"])
        #process keys
        self.process_keys_found(keys=keys_base_entities, depth=configurations["depth"])
        
    def get_keys_entities(self, keys):
        """
        Return the entities for the given group of keys
        :param search keys
        :return:Array with all Keys found by TextRazor
        """
        print("Analizando Claves de Busqueda")
        entity_recognizer = EntityRecognizer()
        recognized_entities = entity_recognizer.recognize_from_text(keys, umbral=0, limit=10)
        print("Analizando Claves de Busqueda - Finalizado")
        return recognized_entities

    def process_keys_found(self, keys = [], depth = 1):
        for key in keys:
            #Build triple with In DBPedia based on entities and depth
            triples_by_key = client.gen_graph_for_neo(key["entity"],depth)
            #Store in Neo4J each triple
            self.process_massive_save_by_key(triples_by_key)
            
    def process_massive_save_by_key(self, triples_by_key):
        for triple in triples_by_key:
            try:
                e1 = Entidad.nodes.get_or_none(name=triple[0])
                if e1 is None:
                    e1 = Entidad(name=triple[0])
                    e1.save()
                e2 = Entidad.nodes.get_or_none(name=triple[2])
                if e2 is None:
                    e2 = Entidad(name=triple[2])
                    e2.save()
                if triple[1] == SUBJECT:
                    rel = e1.subject.relationship(e2)
                    if rel is None:
                        m = e1.subject.connect(e2)
                        m.save()
                if triple[1] == BROADER:
                    rel = e1.broader.relationship(e2)
                    if rel is None:
                        m = e1.broader.connect(e2)
                        m.save()
            except Exception, e:
                print e
                pass

builder = GraphBuilder()
builder.build({u'keys': u'pesticide', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
builder.build({u'keys': u'treatment', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
builder.build({u'keys': u'residue', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
builder.build({u'keys': u'pesticide treatment', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
builder.build({u'keys': u'pesticide residue', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
builder.build({u'keys': u'residue treatment', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
builder.build({u'keys': u'pesticide residue treatment', u'depth':7, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})