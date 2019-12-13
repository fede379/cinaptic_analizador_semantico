from GraphGen import GraphGen
from cinaptic.cinaptic.api.library.semantic.clients.textrazorClient import TextRazorClient
from operator import itemgetter
from utils import loadPickle, getLexicographicTuple
from functools import reduce

graphgen = GraphGen()


class QueryExpansion():
    def execute(self, sk):
        try:
            entitiesTuples = self.getTuplesFromSK(sk)
            if len(entitiesTuples) > 0:
                # aca hacer la magia
                print(entitiesTuples)
                [graphgen.executeEntityTuple(et) for et in entitiesTuples]
                results = self.getResults(entitiesTuples)
                # print(results)
                print("Entity, Weight")
                [print(f"{x[0]}, {x[1]}") for x in results['results']]
                return results
            else:
                print("No se encontraron entidades en la sk...")
        except Exception as e:
            print(e)
            

    def getTuplesFromSK(self, sk):
        tuplesList = []
        if sk is not None:
            print(self.getEntitiesFromSK(sk))
            tuplesList = graphgen.getLexicographicOrderedTuplesList(
                self.getEntitiesFromSK(sk))
        return tuplesList

    def getEntitiesFromSK(self, sk):
        entitiesList = []
        if sk is not None:
            entities = graphgen.getTextRazorResponseFromSK(sk)
            entitiesList = [graphgen.parseTupleToDict(x) for x in entities]
        return entitiesList

    def loadList(self, tupla=(None, None)):
        try:
            lexTupla = getLexicographicTuple(tupla[0], tupla[1])
            nameGraph = f"""{lexTupla[0]}-{lexTupla[1]}"""
            pf = loadPickle(nameGraph)
            return pf['results'], pf['headers']
        except Exception as e:
            print("loadList", e)
            return {}, ()

    def mergeList(self, list1=[], list2=[]):
        if len(list1) > 0 and len(list2) > 0:
            allItems = [*list1, *list2]
            mergedItems = [[x[0], (0 if (x[1] is None) else x[1]) + (0 if (y[1] is None) else y[1])] for x in list1 for y in list2 if x[0] == y[0]]
            aux = [x[0] for x in mergedItems]
            filteredItems = [x for x in allItems if x[0] not in aux]
            result = [*filteredItems, *mergedItems]
            return sorted(result, key=itemgetter(1), reverse=True)
        if len(list1) > 0:
            return list1
        else:
            return list2

    def getResults(self, tuplesList=[]):
        try:
            if len(tuplesList) == 1:
                res, head = self.loadList(tuplesList[0])
                return {'results': res}
            return reduce(lambda x, y: self.mergeTupleResult(x, y), tuplesList)
        except Exception as e:
            print("getResults", e)
            return {'results': []}

    def mergeTupleResult(self, x=[], y=[]):
        try:
            if 'results' not in x:
                xl, h1 = self.loadList(x)
            else:
                xl = x['results']
            if 'results' not in y:
                yl, h2 = self.loadList(y)
            else:
                yl = y['results']
            return {'results': self.mergeList(xl, yl)}
        except Exception as e:
            print("mergeTupleResult", e)
            return {'results': []}


#tuplesList = [
#    ('Paella', 'Risotto'),
#    ('Rice', 'Risotto'),
#    ('Pilaf', 'Biryani')
#]
#qe = QueryExpansion()
#
#print(qe.getResults(tuplesList))
#list1, h = qe.loadList(tuplesList[0])
#list2, h2 = qe.loadList(tuplesList[1])
#print(list1)
#print(list2)
#print(qe.mergeList(list1, list2))
# ent = qe.execute('water quality monitoring algae image processing')
# print(ent)

# print(loadPickle('Algae-Water quality'))
