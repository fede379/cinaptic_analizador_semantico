from SPARQLWrapper import SPARQLWrapper, JSON
import logging
import json
from cinaptic.cinaptic.api.library.semantic.repository.Neo4J import *
from neomodel import db
from pypher import Pypher, __

# import time

TYPE = "type"
ENTITY = "entity"
VALUE = "value"
INCOMING = "incoming"
OUTCOMING = "outcoming"


SLASH_RESOURCE = "/resource/"
CATEGORY_RESOURCE = "/Category:"
DBPEDIA_SPARKQL_ENDPOINT = "http://dbpedia.org/sparql"
logger = logging.getLogger()
p = Pypher()


class DBPedia:
    def execute(self, entity):
        incoming_relations = []
        outcoming_relations = []
        relations = []
        try:
            resource_entity = f"""dbr:{entity}"""
            query = self.buildQuery(resource_entity)
            sparql = SPARQLWrapper(DBPEDIA_SPARKQL_ENDPOINT)
            sparql.setQuery(query=query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            entities = results["results"]["bindings"]
            relations = list(map(lambda x: self.parseEntities(x), entities))
            self.persistData(idGraph=f"{entity}-allrelations", mainEntity=entity, relations=relations)
            # json file
            exDict = {'results': entities}
            with open('dbpedia-query.json', 'w') as file:
                file.write(json.dumps(exDict))
            exDict = {'relations': relations}
            with open('relations.json', 'w') as file:
                file.write(json.dumps(exDict))
            incoming_relations = list(filter(lambda x: x['direction'] == 'incoming', relations))
            outcoming_relations = list(filter(lambda x: x['direction'] == 'outcoming', relations))
        except Exception as e:
            logger.error(e)
            pass        
        return incoming_relations, outcoming_relations

    def buildQuery(self, resource_entity):
        return f"""
            PREFIX  dbc:  <http://dbpedia.org/resource/Category:>
            PREFIX  dbr: <http://dbpedia.org/resource/>
            PREFIX  owl: <http://www.w3.org/2002/07/owl#>
            PREFIX  dbo: <http://dbpedia.org/ontology/>
            SELECT * WHERE {{
                {{SELECT * WHERE {{
                {resource_entity} ?outcoming ?value. FILTER( STRSTARTS(STR(?value),str(dbc:)) || STRSTARTS(STR(?value),str(dbr:)) || STRSTARTS(STR(?value),str(owl:)) || STRSTARTS(STR(?value),str(dbo:)) )    
            }}}} UNION {{
                    SELECT * WHERE {{
                        ?value ?incoming {resource_entity}. FILTER( STRSTARTS(STR(?value),str(dbc:)) || STRSTARTS(STR(?value),str(dbr:)) || STRSTARTS(STR(?value),str(owl:)) || STRSTARTS(STR(?value),str(dbo:)) )
                    }}
                }}
            }}
        """

    def parseEntities(self, dbpedia_entity):
        keys_entity = dbpedia_entity.keys()
        entity = {}
        if OUTCOMING in keys_entity:
            entity['direction'] = OUTCOMING
            entity['relation'] = self.parseNode(
                url=dbpedia_entity[OUTCOMING][VALUE])
        else:
            entity['direction'] = INCOMING
            entity['relation'] = self.parseNode(
                url=dbpedia_entity[INCOMING][VALUE])
        entity['node'] = self.parseNode(url=dbpedia_entity[VALUE][VALUE])
        return entity

    def parseNode(self, url):
        node = ''
        if '#' in url:
            node = url[url.rfind('#') + 1:]
        else:
            if CATEGORY_RESOURCE in url:
                index = url.rfind(':')
                node = url[index + 1:]
            else:
                if '/' in url:
                    index = url.rfind('/')
                    node = url[index + 1:]
        return node
    
    def persistData(self, idGraph, mainEntity, relations):
        try:
            p.MERGE.node('e1', 'Entidad', name=mainEntity, idGraph=idGraph)
            db.cypher_query(str(p), params=p.bound_params)
            list(map(lambda x: self.saveTriple(mainEntity, x, idGraph), relations))
        except Exception as e:
            print(e)
            pass

    def saveTriple(self, mainEntity, triple, idGraph):
        try:
            p.reset()
            if triple['node'] != mainEntity:
                if triple['direction'] == 'outcoming':                
                    p.MATCH.node('e1', 'Entidad', name=mainEntity, idGraph=idGraph).MERGE.node('e1').rel_out(labels=str(triple['relation']).upper()).node('e2', 'Entidad', name=triple['node'], idGraph=idGraph)
                if triple['direction'] == 'incoming':
                    p.MATCH.node('e1', 'Entidad', name=mainEntity, idGraph=idGraph).MERGE.node('e2', 'Entidad', name=triple['node'], idGraph=idGraph).rel_out(labels=str(triple['relation']).upper()).node('e1')
            else:
                p.MATCH.node('e1', 'Entidad', name=mainEntity, idGraph=idGraph).MERGE.node('e1').rel_out(labels=str(triple['relation']).upper()).node('e1')
            db.cypher_query(str(p), params=p.bound_params)
            return str(p)
        except Exception as e:
            print(e)
            pass


dbpedia = DBPedia()
incomings, outcomings = dbpedia.execute('Water_quality')
print(f"{len(incomings)} entrantes")
print(f"{len(outcomings)} salientes")

# mainEntity = 'Water'
# idGraph = 'test'
# relation = 'TEST'
# node = 'Test'
# p.MATCH.node('e1', 'Entidad', name=mainEntity, idGraph=idGraph).MERGE.node('e1').rel_out(labels=relation).node('e2', 'Entidad', name=node, idGraph=idGraph)
# p.MERGE.node(mainEntity, 'Entidad', name=mainEntity, idGraph=idGraph).rel_out(labels='RELACION').node('entity2', 'Entidad', name='Test', idGraph=idGraph)
# aux = db.cypher_query(str(p), params=p.bound_params)
# print(aux)

# print(node)
