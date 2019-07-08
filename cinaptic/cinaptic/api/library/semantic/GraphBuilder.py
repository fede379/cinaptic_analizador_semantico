# from EntityRecognizer import EntityRecognizer
# from EntitiesMapper import EntityMapper
# from Analyzer import Analyser
from .CypherQueries import CypherQueries
from .clients.DBPedia import * 
from .repository.Neo4J import *
from neomodel import db
from .utils.Email import EmailSender
import logging
client = DBPedia()
cypherQueries = CypherQueries()
emailService = EmailSender()
SUBJECT = 'subject'
BROADER = 'broader'
SINONYM = 'sinonym'
RELATIONS = [SUBJECT.upper(), BROADER.upper()]

logger = logging.getLogger()

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class GraphBuilder:
    def build(self, configurations):
        #Get with Text Razor the entities
        #keys_base_entities = self.get_keys_entities(configurations["keys"])
        #process keys
        start = time.time()
        print("START")
        logger.info("Start!")
        self.process_keys_found(key=configurations["entity"], depth=configurations["depth"])
        self.process_results(key=configurations["entity"])
        end = time.time()
        print("Time elapsed: {0}".format(end-start))
        logger.info("Time elapsed: {0}".format(end-start))

    def gen_graph_for_neo(self, entity, depth):
        print("ALMACENANDO NIVEL: {0}".format(0))
        logger.info("ALMACENANDO NIVEL: {0}".format(0))
        triples_by_key, entities_not_processed = client.execute(entity)
        self.process_massive_save_by_key(triples_by_key, entity)
        entities_processed = []
        entities_processed.append(entity)
        for i in range(0,depth):
            print("ALMACENANDO NIVEL: {0}".format(i + 1))
            logger.info("ALMACENANDO NIVEL: {0}".format(i + 1))
            lvl = []
            for ent in entities_not_processed:
                if(ent not in entities_processed):
                    triples_by_key, lvl = client.execute(ent)
                    self.process_massive_save_by_key(triples_by_key, entity)
                    entities_processed.append(ent)
                    print("Entidades procesadas: "+str(len(entities_processed)))
                    logger.info("Entidades procesadas: "+str(len(entities_processed)))
                    entities_not_processed = list(set(entities_not_processed + lvl))

    def process_keys_found(self, key = "", depth = 1):
        #Build triple with In DBPedia based on entities and depth
        triples_by_key = self.gen_graph_for_neo(key, depth)
        #Store in Neo4J each triple

    def process_results(self, key=''):
        files = []
        for rel in RELATIONS:
            files.append(cypherQueries.closeness_algo(key, rel, False))
            files.append(cypherQueries.closeness_harmonic_algo(key, rel))
            files.append(cypherQueries.closeness_algo(key, rel, True))
            files.append(cypherQueries.betweenness_algo(key, rel))
            files.append(cypherQueries.pageRank_algo(key, rel, 20, 0.85))
        emailService.sendMailToAll(info=f"Proceso terminado. Resultados del grafo {key}:", filesToSend=files, error=False)
            
    def process_massive_save_by_key(self, triples_by_key, nameGraph):
        for triple in triples_by_key:
            print(triple)
            logger.info(triple)
            try:
                e1 = Entidad.nodes.get_or_none(name=triple[0], idGraph=nameGraph)
                if e1 is None:
                    e1 = Entidad(name=triple[0], idGraph= nameGraph)
                    e1.save()
                e2 = Entidad.nodes.get_or_none(name=triple[2], idGraph=nameGraph)
                if e2 is None:
                    e2 = Entidad(name=triple[2], idGraph=nameGraph)
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
            except Exception as e:
                print(e)
                emailService.sendMailToAdmin(e)
                pass


# builder = GraphBuilder()
#builder.build({u'keys': u'Pesticide', u'depth':5, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
#builder.build({u'keys': u'Treatment', u'depth':5, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
# builder.build({u'keys': u'Pesticide', u'depth':2, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
#builder.build({u'keys': u'Pesticide_residue', u'depth':3, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
#builder.build({u'keys': u'Pesticide_treatment', u'depth':5, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
#builder.build({u'keys': u'Residue_treatment', u'depth':5, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
#builder.build({u'keys': u'Pesticide_residue_treatment', u'depth':5, u'engines': [{u'engine': u'google', u'number_of_urls': 10, u'number_of_pages': 10, u'limit': 15, u'umbral': 0.1}], u'max_graph_level': 7})
