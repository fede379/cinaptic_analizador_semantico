from SPARQLWrapper import SPARQLWrapper, JSON
import logging
import json
from .cinaptic.cinaptic.api.library.semantic.repository.Neo4J import *
from neomodel import db

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
            # json file
            exDict = {'results': entities}
            with open('dbpedia-query.json', 'w') as file:
                file.write(json.dumps(exDict))
            exDict = {'relations': relations}
            with open('relations.json', 'w') as file:
                file.write(json.dumps(exDict))
            # print(relations)
            # print(len(relations))
        except Exception as e:
            logger.error(e)
            pass
        try:
            print(
                f"{len(incoming_relations)} Relaciones entrantes encontradas para: {entity}")
            print(
                f"{len(outcoming_relations)} Relaciones salientes encontradas para: {entity}")
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

    def saveTriples(self, mainEntity, relations)
        


dbpedia = DBPedia()
incomings, outcomings = dbpedia.execute('Water')



# url = "http://dbpedia.org/resource/Category:Liquids"
# url = "http://dbpedia.org/resource/Constituent"
# url = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
# if '#' in url:
#     node = url[url.rfind('#') + 1:]
# else:    
#     if CATEGORY_RESOURCE in url:
#         index = url.rfind(':')
#         node = url[index + 1:]
#     else:
#         if '/' in url:
#             index = url.rfind('/')
#             node = url[index + 1:]

# print(node)
