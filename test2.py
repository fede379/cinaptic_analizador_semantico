from SPARQLWrapper import SPARQLWrapper, JSON
import json
from cinaptic.cinaptic.api.library.semantic.repository.Neo4J import *
from neomodel import db
from cinaptic.cinaptic.api.library.semantic.clients.textrazorClient import *
from operator import itemgetter

DBPEDIA_SPARKQL_ENDPOINT = "http://dbpedia.org/sparql"
WIKIPEDIA_URLBASE = "http://en.wikipedia.org/wiki/"
textrazorclient = TextRazorClient()

class EntityExtraction:
    def __init__(self):
        self.seen = set()
        print('init')

    def getListEntitiesFromWiki(self, entity = None, top = None):
        # urls = self.getWikipediaUrls(entity)
        # listEntitiesFromWiki = list(map(lambda x: self.getTextRazorResponse(x), urls))
        entitiesFromWiki = []
        if entity is not None:
            url = f"{WIKIPEDIA_URLBASE}{entity}"
            entitiesFromWiki = self.getTextRazorResponse(url)
            entidadesWiki = list(map(lambda x: self.parseTupleToDict(x), entitiesFromWiki))
            sortedListEntities = sorted(entidadesWiki, key=itemgetter('relevance'), reverse=True)
            # only for duplicate filter purposes
            self.seen = set()
            # only for duplicate filter purposes
            withoutDuplicates = list(filter(lambda x: self.avoidDuplicate(x), sortedListEntities))
            withoutRelevanceZero = list(filter(lambda x: x["relevance"] > 0, withoutDuplicates))
        return withoutRelevanceZero[:top] if top is not None else withoutRelevanceZero
        
    def avoidDuplicate(self, eldict):
        if eldict['id'] in self.seen:
            return False
        self.seen.add(eldict['id'])
        return True

    # def getWikipediaUrls(self, entity):
    #     query = self.buildQuery(entity)
    #     sparql = SPARQLWrapper(DBPEDIA_SPARKQL_ENDPOINT)
    #     sparql.setQuery(query=query)
    #     sparql.setReturnFormat(JSON)
    #     results = sparql.query().convert()
    #     urls = list(map(lambda x: self.parseDbpediaResponse(x),
    #                     results['results']['bindings']))
    #     return urls

    def parseDbpediaResponse(self, result=None):
        if (result is not None):
            return result['wikiurl']['value']
        return ''

    def buildQuery(self, entity):
        return f"""
        SELECT ?wikiurl
        WHERE {{
            dbr:{entity} foaf:isPrimaryTopicOf ?wikiurl
        }}
        """

    def getTextRazorResponse(self, url=None):
        textRazorResponse = {}
        if url is not None:
            textRazorResponse = set(map(lambda x: self.parseTextRazorResponse(x), set(textrazorclient.get_entities_from_url(url).entities())))
        return textRazorResponse

    def parseTextRazorResponse(self, textRazorResponse=None):
        responseDict = ()
        if textRazorResponse is not None:
            responseDict = (
                textRazorResponse.id,
                textRazorResponse.confidence_score,
                textRazorResponse.relevance_score,
                textRazorResponse.wikipedia_link,
            )
        return responseDict

    def parseTupleToDict(self, tupla = None):
        """
        pasamos de set(para eliminar duplicados) a lista para trabajarlos con mas comodidad
        """
        responseDict = {}
        if tupla is not None:
            responseDict = {
                "id": tupla[0],
                "confidence": tupla[1],
                "relevance": tupla[2],
                "wikiurl": tupla[3]
            }
        return responseDict
    
    def directMatchingList(self, listEntity1 = [], listEntity2 = []):
        idList = list(map(lambda x: x['id'], listEntity2))
        return list(filter(lambda x: x['id'] in idList, listEntity1))

    def calculateWeights(self, index, entityDict, listLength):
        entityDict['weight'] = (1 / (index + 1))
        return entityDict

enex = EntityExtraction()
entity1 = 'Water_quality'
listEntity1 = enex.getListEntitiesFromWiki(entity1, 50)
entity2 = 'Water'
listEntity2 = enex.getListEntitiesFromWiki(entity2, 50)
result = enex.directMatchingList(listEntity1, listEntity2)
eljson = {
    entity1: listEntity1,
    entity2: listEntity2,
    'results': result
    }
# print(eljson)
# print(len(result))
with open(f'{entity1}-{entity2}-textRazorEntity.json', 'w') as file:
    file.write(json.dumps(eljson))