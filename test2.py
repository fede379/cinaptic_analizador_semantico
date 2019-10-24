from SPARQLWrapper import SPARQLWrapper, JSON
import json
from cinaptic.cinaptic.api.library.semantic.repository.Neo4J import *
from neomodel import db
from cinaptic.cinaptic.api.library.semantic.clients.textrazorClient import *
from operator import itemgetter
import wikipedia
from functools import reduce

WEIGHTS = [1.0, 0.5, 0.3333333333333333, 0.25, 0.2, 0.16666666666666666, 0.14285714285714285, 0.125, 0.1111111111111111, 0.1, 0.09090909090909091, 0.08333333333333333, 0.07692307692307693, 0.07142857142857142, 0.06666666666666667, 0.0625, 0.058823529411764705, 0.05555555555555555, 0.05263157894736842, 0.05, 0.047619047619047616, 0.045454545454545456, 0.043478260869565216, 0.041666666666666664, 0.04, 0.038461538461538464, 0.037037037037037035, 0.03571428571428571, 0.034482758620689655, 0.03333333333333333, 0.03225806451612903, 0.03125, 0.030303030303030304, 0.029411764705882353, 0.02857142857142857, 0.027777777777777776, 0.02702702702702703, 0.02631578947368421, 0.02564102564102564, 0.025, 0.024390243902439025, 0.023809523809523808, 0.023255813953488372, 0.022727272727272728, 0.022222222222222223, 0.021739130434782608, 0.02127659574468085, 0.020833333333333332, 0.02040816326530612, 0.02, 0.0196078431372549, 0.019230769230769232, 0.018867924528301886,
           0.018518518518518517, 0.01818181818181818, 0.017857142857142856, 0.017543859649122806, 0.017241379310344827, 0.01694915254237288, 0.016666666666666666, 0.01639344262295082, 0.016129032258064516, 0.015873015873015872, 0.015625, 0.015384615384615385, 0.015151515151515152, 0.014925373134328358, 0.014705882352941176, 0.014492753623188406, 0.014285714285714285, 0.014084507042253521, 0.013888888888888888, 0.0136986301369863, 0.013513513513513514, 0.013333333333333334, 0.013157894736842105, 0.012987012987012988, 0.01282051282051282, 0.012658227848101266, 0.0125, 0.012345679012345678, 0.012195121951219513, 0.012048192771084338, 0.011904761904761904, 0.011764705882352941, 0.011627906976744186, 0.011494252873563218, 0.011363636363636364, 0.011235955056179775, 0.011111111111111112, 0.01098901098901099, 0.010869565217391304, 0.010752688172043012, 0.010638297872340425, 0.010526315789473684, 0.010416666666666666, 0.010309278350515464, 0.01020408163265306, 0.010101010101010102, 0.01]
DBPEDIA_SPARKQL_ENDPOINT = "http://dbpedia.org/sparql"
WIKIPEDIA_URLBASE = "http://en.wikipedia.org/wiki/"
textrazorclient = TextRazorClient()


class EntityExtraction:
    def __init__(self):
        self.entitiesSeen = set()
        self.tuplesSeen = set()
        self.computed = set()
        self.remnants = set()

    def getListEntitiesFromWiki(self, entity=None, top=None):
        entitiesFromWiki = []
        if entity is not None:
            entitiesFromWiki = self.getTextRazorResponse(entity)
            entidadesWiki = list(
                map(lambda x: self.parseTupleToDict(x), entitiesFromWiki))
            sortedListEntities = sorted(entidadesWiki, key=itemgetter(
                'relevance', 'confidence'), reverse=True)
            # only for duplicate filter purposes
            self.entitiesSeen = set()
            # only for duplicate filter purposes
            withoutDuplicates = list(
                filter(lambda x: self.avoidDuplicate(x), sortedListEntities))
            withoutRelevanceZero = list(
                filter(lambda x: x["relevance"] > 0, withoutDuplicates))
        return withoutRelevanceZero[:top] if top is not None else withoutRelevanceZero

    def avoidDuplicate(self, entity):
        if entity['id'] in self.entitiesSeen:
            return False
        self.entitiesSeen.add(entity['id'])
        return True

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

    def getTextRazorResponse(self, entity=None):
        textRazorResponse = {}
        if entity is not None:
            # textRazorResponse = set(map(lambda x: self.parseTextRazorResponse(x), set(textrazorclient.get_entities_from_url(url).entities())))
            textRazorResponse = set(map(lambda x: self.parseTextRazorResponse(x), set(
                textrazorclient.get_entities_from_text(self.getContentFromWiki(entity)).entities())))
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

    def parseTupleToDict(self, tupla=None):
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

    def getDirectMatchingList(self, listEntity1=[], listEntity2=[], top=None):
        idList1 = list(map(lambda x: x['id'], listEntity1))
        listMatched = list(filter(lambda y: y is not None, map(lambda x: self.matching(
            x, x['id'] in idList1, listEntity1, listEntity2), listEntity2)))
        sortedListMatched = sorted(
            listMatched, key=itemgetter('relevance'), reverse=True)
        return sortedListMatched[:top] if top is not None else sortedListMatched

    def calculateWeight(self, value1=0, value2=0, index1=0, index2=0):
        return (value1 * WEIGHTS[index1]) + (value2 * WEIGHTS[index2])

    def matching(self, entity=None, isMatch=False, listEntity1=[], listEntity2=[]):
        if entity is not None and isMatch:
            item1 = next(
                (item for item in listEntity1 if item['id'] == entity['id']), None)
            item2 = next(
                (item for item in listEntity2 if item['id'] == entity['id']), None)
            if item1 is not None and item2 is not None:
                return {
                    "id": entity['id'],
                    "relevance": self.calculateWeight(item1['relevance'], item2['relevance'], listEntity1.index(item1), listEntity2.index(item2)),
                    "wikiurl": entity['wikiurl']
                }
        return None

    def getContentFromWiki(self, entity=None):
        if entity is not None:
            try:
                wp = wikipedia.page(title=entity)
                return wp.content
            except Exception as e:
                print(e)
                pass
        return ''

    def computeTuple(self, tupla=(None, None), topTR=None, topMatching=None):
        result = []
        if tupla[0] is not None and tupla[1] is not None:
            listEntity1 = self.getListEntitiesFromWiki(tupla[0], topTR)
            listEntity2 = self.getListEntitiesFromWiki(tupla[1], topTR)
            result = self.getDirectMatchingList(
                listEntity1, listEntity2, topMatching)
        return result

    def getTuplesFromResults(self, matchingList=[]):
        try:
            mlistIds = [entity['id'] for entity in matchingList]
            mlistIdsOrdered = sorted(mlistIds)
            result = [(x, y) for x in mlistIdsOrdered for y in mlistIdsOrdered if x < y]
        except Exception as e:
            print(e)
            result = set()
            pass
        return result



# enex = EntityExtraction()
# entity1 = 'Golden_Retriever'
# entity2 = 'Pug'
# top = 100
# topMatching = 3
# result = enex.computeTuple((entity1, entity2), top)
# eljson = {
#     'results': result
#     }
# with open(f'{entity1}-{entity2}-textRazorEntity({top}).json', 'w') as file:
#     file.write(json.dumps(eljson))

# test = [
#     {
#         "id": "Purebred dog",
#         "relevance": 0.23144,
#         "wikiurl": "http://en.wikipedia.org/wiki/Purebred_dog"
#     },
#     {
#         "id": "American Kennel Club",
#         "relevance": 0.1456233333333333,
#         "wikiurl": "http://en.wikipedia.org/wiki/American_Kennel_Club"
#     },
#     {
#         "id": "Dog",
#         "relevance": 0.10907857142857143,
#         "wikiurl": "http://en.wikipedia.org/wiki/Dog"
#     }
# ]

# enex.getTuplesFromResults(test)
# print(enex.getTuplesFromResults(test))
# cosas = []
# mascosas = tuple(set(['aaa', 'bbb']))
# muy = tuple(set(['locas', 'cosas']))
# locas = tuple(set(['cosas', 'locas']))
# pasan = tuple(set(['pasan', 'cosas']))
# locass = tuple(set(['cosass', 'locass']))
# cosas.append(mascosas)
# print(cosas)
# cosas.append(muy)
# print(cosas)
# cosas.append(locass)
# print(cosas)
# cosas.append(locas)
# print(cosas)
# cosas.append(pasan)
# print(cosas)
# cosas.remove(locas)
# print(cosas)
