from EntityRecognizer import EntityRecognizer
from EntitiesMapper import EntityMapper
from Analyzer import Analyser
from clients.DBPedia import * 
from repository.Neo4J import *
import logging
client = DBPedia()
SUBJECT = 'subject'
BROADER = 'broader'
SINONYM = 'sinonym'
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class GraphBuilder:
    def build(self, configurations):
        #Get with Text Razor the entities
        #keys_base_entities = self.get_keys_entities(configurations["keys"])
        #process keys
        start = time.time()
        print("START")
        self.process_keys_found(key=configurations["keys"], depth=configurations["depth"])
        end = time.time()
        print("Time elapsed: {0}".format(end-start))


    def gen_graph_for_neo(self,entity, depth):
        print("ALMACENANDO NIVEL: {0}".format(0))
        triples_by_key, entities_not_processed = client.execute(entity)
        self.process_massive_save_by_key(triples_by_key, 0)
        entities_processed = []
        entities_processed.append(entity)
        for i in range(0,depth):
            print("ALMACENANDO NIVEL: {0}".format(i + 1))
            lvl = []
            for ent in entities_not_processed:
                if(ent not in entities_processed):
                    triples_by_key, lvl = client.execute(ent)
                    self.process_massive_save_by_key(triples_by_key, i+1)
                    entities_processed.append(ent)
                    #print("Entidades procesadas: "+len(entities_processed))
                    entities_not_processed = list(set(entities_not_processed + lvl))

    def process_keys_found(self, key = "", depth = 1):
        #Build triple with In DBPedia based on entities and depth
        triples_by_key = self.gen_graph_for_neo(key,depth)
        #Store in Neo4J each triple
            
    def process_massive_save_by_key(self, triples_by_key, k):
        for triple in triples_by_key:
            print(triple)
            logging.debug(triple)
            try:
                e1 = Entidad.nodes.get_or_none(name=triple[0])
                if e1 is None:
                    e1 = Entidad(name=triple[0])
                    e1.save()
                e2 = Entidad.nodes.get_or_none(name=triple[2])
                if e2 is None:
                    e2 = Entidad(name=triple[2])
                    e2.save()
                if triple[1] == SINONYM:
                    rel = e1.sinonym.relationship(e2)
                    if rel is None:
                        m = e1.sinonym.connect(e2)
                        m.save()
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
#builder.build({u'keys': u'Pesticide', u'depth':5, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
#builder.build({u'keys': u'Treatment', u'depth':5, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
builder.build({u'keys': u'Residue', u'depth':3, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
#builder.build({u'keys': u'Pesticide_residue', u'depth':3, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
#builder.build({u'keys': u'Pesticide_treatment', u'depth':5, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
#builder.build({u'keys': u'Residue_treatment', u'depth':5, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
#builder.build({u'keys': u'Pesticide_residue_treatment', u'depth':5, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})