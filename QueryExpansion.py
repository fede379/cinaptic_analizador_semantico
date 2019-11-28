from GraphGen import GraphGen
from cinaptic.cinaptic.api.library.semantic.clients.textrazorClient import TextRazorClient
from operator import itemgetter

graphgen = GraphGen()

class QueryExpansion():
    def execute(self, sk):
        if sk is not None:
            entitiesTuples = self.getTuplesFromSK(sk)
            if len(entitiesTuples) > 0:
                # aca hacer la magia
                # [graphgen.executeEntityTuple(et) for et in entitiesTuples]
                print(entitiesTuples)
            return entitiesTuples

    def getTuplesFromSK(self, sk):
        tuplesList = []
        if sk is not None:
            tuplesList = graphgen.getLexicographicOrderedTuplesList(self.getEntitiesFromSK(sk))
        return tuplesList

    def getEntitiesFromSK(self, sk):
        entitiesList = []
        if sk is not None:
            entities = graphgen.getTextRazorResponseFromSK(sk)
            entitiesList = [graphgen.parseTupleToDict(x) for x in entities]
        return entitiesList


# qe = QueryExpansion()
# ent = qe.execute('water quality monitoring algae image processing')
# print(ent)