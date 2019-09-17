from SPARQLWrapper import SPARQLWrapper, JSON
import json
from cinaptic.cinaptic.api.library.semantic.repository.Neo4J import *
from neomodel import db
from cinaptic.cinaptic.api.library.semantic.clients.textrazorClient import *
from operator import itemgetter

DBPEDIA_SPARKQL_ENDPOINT = "http://dbpedia.org/sparql"
WIKIPEDIA_URLBASE = "http://en.wikipedia.org/wiki/"
textrazorclient = TextRazorClient()
SEEN = set()

class EntityExtraction:
    def getListEntitiesFromWiki(self, entity = None):
        # urls = self.getWikipediaUrls(entity)
        # listEntitiesFromWiki = list(map(lambda x: self.getTextRazorResponse(x), urls))
        entitiesFromWiki = []
        if entity is not None:
            url = f"{WIKIPEDIA_URLBASE}{entity}"
            entitiesFromWiki = self.getTextRazorResponse(url)
            entidadesWiki = list(map(lambda x: self.parseTupleToDict(x), entitiesFromWiki))
            sortedListEntities = sorted(entidadesWiki, key=itemgetter('relevance'), reverse=True)
            # only for duplicate filter purposes
            SEEN = set()
            withoutDuplicates = list(filter(lambda x: self.avoidDuplicate(x), sortedListEntities))
            result = list(filter(lambda x: x["relevance"] > 0, withoutDuplicates))
        return result[:10]
        
    def avoidDuplicate(self, eldict):
        if eldict['id'] in SEEN:
            return False
        SEEN.add(eldict['id'])
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

enex = EntityExtraction()
entity = 'Water_quality'
result = enex.getListEntitiesFromWiki(entity)
eljson = {'results': result}
# print(eljson)
print(len(result))
with open(f'{entity}-textRazorEntity.json', 'w') as file:
    file.write(json.dumps(eljson))

# lista = [("hola", 12, 12.3, "mundo"), ("hola2", 13, 15.3, "mundo2")]
# myfset = set(lista)

# print(list(myfset))