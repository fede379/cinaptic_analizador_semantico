from functools32 import lru_cache

from clients.dbpediaClient import DBPediaClient
from clients.consts import *
from utils.utils import concat_arrays

dbpedia_client = DBPediaClient()
class GraphGenerator:

    @lru_cache(maxsize=5000)
    def build(self, entity=None, levels=1):
        grafo = []
        already_expanded = []
        entities = []
        if(entity is not None):
            entities.append({'relation': 0, 'name': entity, "level":0})
            for i in range(levels):
                grafo, entities, already_expanded = self.get_graph_level(grafo, entities, already_expanded, i)

        print("<<<<<< FIN >>>>>>")
        return grafo

    def get_graph_level(self, grafo, entities, already_expanded_in, i):

        aux = []
        for entity in entities:
            if entity[NAME] not in already_expanded_in:
                print("Expadiendo Entidad: " + entity[NAME])
                nodes = dbpedia_client.get_entities(field=IS_OF_RELATIONS, field_type=IS_BROADER_TYPE,
                                                               entity=entity[NAME], is_broader_flag=True, level=i)
                grafo.append({entity[NAME]: nodes})
                already_expanded_in.append(entity[NAME])
                aux = concat_arrays([nodes, aux])
        entities = concat_arrays([entities, aux])

        return grafo, entities, already_expanded_in

    def get_ratio(self, key, grafo):
        arreglo_entidad = self.get_nodes(grafo)
        arreglo_keys = self.get_nodes(key)
        aes = []
        for i, ae in enumerate(grafo):
            for j, ak in enumerate(key):
                if (ae == ak):
                    aes.append(ae)

        denominador = len(arreglo_entidad) + len(arreglo_keys)
        numerador = len(aes)
        ratio = float(numerador) / (float(denominador) - float(numerador))
        print(aes)
        print("ratio: {0} / {1} = {2}".format(numerador, denominador, ratio))
        return ratio

    def get_nodes(self, dic):
        res = []
        for key in dic.keys():
            res.append(key)

        return res



#test = GraphGenerator()
#grafo = test.build("Machine_learning", 3)
#print(grafo)
#print(calcular_grafo(grafo))