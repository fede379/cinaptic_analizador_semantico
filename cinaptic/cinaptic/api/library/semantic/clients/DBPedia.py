from SPARQLWrapper import SPARQLWrapper, JSON
from .consts import DBPEDIA_SPARKQL_ENDPOINT, \
    RESULTS, BINDINGS, VALUE, ARISTS_VALUE, NAME, \
    RELATION, SLASH_RESOURCE, TWO_POINTS
import time
import logging
IS_BROADER_OF = "is_broader_of"
BROADER = "broader"

IS_SUBJECT_OF = "is_subject_of"
SUBJECT = "subject"

SINONYM = 'sinonym'

TYPE = "type"
ENTITY = "entity"
VALUE = "value"

SLASH_RESOURCE = "/resource/"
CATEGORY_RESOURCE = "/Category:"

logger = logging.getLogger()

class DBPedia:
    def execute(self, entity):
        level_entities = []
        relations = []
        try:
            category_entity = "http://dbpedia.org/resource/Category:{0}".format(entity)
            resource_entity = "http://dbpedia.org/resource/{0}".format(entity)
            query = self.buildQuery(category_entity, resource_entity)
            sparql = SPARQLWrapper(DBPEDIA_SPARKQL_ENDPOINT)
            sparql.setQuery(query=query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            entities = results["results"]["bindings"]
            if len(entities)>0:
                for json_entity in entities:
                    tp = json_entity[TYPE][VALUE]
                    if CATEGORY_RESOURCE in json_entity[ENTITY][VALUE]:
                        e = json_entity[ENTITY][VALUE].split(CATEGORY_RESOURCE)[1]
                    else: 
                        e = json_entity[ENTITY][VALUE].split(SLASH_RESOURCE)[1]
                    if(e != entity):
                        level_entities.append(e)
                    if tp == SINONYM:
                        e1 = entity
                        e2 = e
                        rel = SINONYM
                    if tp == IS_BROADER_OF or tp == IS_SUBJECT_OF:
                        e1 = entity
                        e2 = e
                        rel = BROADER if IS_BROADER_OF == tp else SUBJECT
                    else:
                        e1 = e
                        e2 = entity
                        rel = BROADER if BROADER == tp else SUBJECT
                    #node = "{e1} ---{rel}--->  {e2}".format(e1=e1, rel=rel, e2=e2)
                    #print(node)
                    relations.append((e1, rel, e2))
        except e:
            logger.error(e)
            pass
        try:
            print("{0} Entidades encontradas para: {1}".format(len(relations), entity))
            logger.info("{0} Entidades encontradas para: {1}".format(len(relations), entity))
        except e:
            logger.error(e)
            pass
        return relations, level_entities

    def buildQuery(self, category_entity, resource_entity):
        query = """
                PREFIX  skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX  dbc:  <http://dbpedia.org/resource/Category:>
                PREFIX  dct:  <http://purl.org/dc/terms/>
                PREFIX  dbr: <http://dbpedia.org/resource/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT  distinct ?entity, ?type
                WHERE {
                    {
                        SELECT  ?entity, 'is_subject_of' as ?type
                        WHERE   { 
                            ?entity dct:subject <"""+category_entity+"""> 
                        }
                    }
                    UNION
                    {
                        SELECT  ?entity, 'is_broader_of' as ?type
                        WHERE   { 
                            ?entity skos:broader <"""+category_entity+"""> 
                        }
                    }
                    UNION
                    {
                        SELECT  ?entity, 'broader' as ?type
                        WHERE { 
                            <"""+category_entity+"""> skos:broader  ?entity 
                        }
                    }
                    UNION
                    { 
                        SELECT  ?entity, 'subject' as ?type
                        WHERE { 
                            <"""+category_entity+"""> dct:subject  ?entity 
                        }
                    }
                    UNION
                    {
                        SELECT  ?entity, 'is_subject_of' as ?type
                        WHERE   { 
                            ?entity dct:subject <"""+resource_entity+"""> 
                        }
                    }
                    UNION
                    {
                        SELECT  ?entity, 'is_broader_of' as ?type
                        WHERE   { 
                            ?entity skos:broader <"""+resource_entity+"""> 
                        }
                    }
                    UNION
                    {
                        SELECT  ?entity, 'broader' as ?type
                        WHERE { 
                            <"""+resource_entity+"""> skos:broader  ?entity 
                        }
                    }
                    UNION
                    { 
                        SELECT  ?entity, 'subject' as ?type
                        WHERE { 
                            <"""+resource_entity+"""> dct:subject  ?entity 
                        }
                    }
                    UNION {
                            SELECT ?entity, 'sinonym' as ?type
                            WHERE 
                            { 
                            {
                            <"""+resource_entity+"""> <http://dbpedia.org/ontology/wikiPageDisambiguates> ?entity.
                            }
                            UNION
                            { 
                            <"""+resource_entity+"""> <http://dbpedia.org/ontology/wikiPageDisambiguates> ?entity.
                            ?x <http://dbpedia.org/ontology/wikiPageDisambiguates> ?entity.
                            }
                            UNION
                            {
                            ?entity <http://dbpedia.org/ontology/wikiPageDisambiguates> <"""+resource_entity+""">.
                            }
                            UNION
                            { 
                            ?entity <http://dbpedia.org/ontology/wikiPageDisambiguates> <"""+resource_entity+""">.
                            ?x <http://dbpedia.org/ontology/wikiPageDisambiguates> ?entity.
                            }
                            }
                    }
                }
        """
        return query

#dbp = DBPedia()
#start = time.time()
#relations, level_entities = dbp.execute('Pesticide', [])
#for i in range(0,5):
#    lvl = []
#    for ent in level_entities:
#        relations, lvl = dbp.execute(ent, relations, lvl)
#    level_entities = list(dict.fromkeys(lvl))
#end = time.time()
#print("Time elapsed: {0}".format(end-start))
#print(relations)
#