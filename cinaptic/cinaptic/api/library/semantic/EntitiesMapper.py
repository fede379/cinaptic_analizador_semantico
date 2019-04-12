from Generator import GraphGenerator
from graphs.graph import find_path
from repository.Neo4J import Neo4J
#from logging import Logger
#from repoze.lru import lru_cache

class EntityMapper:


    def normalize_keys(self, keys=[], levels=1):
        #Logger.debug("Normalizando Claves de Busqueda")
        graph_generator = GraphGenerator()
        keys_entities = []
        for i, key in enumerate(keys):
        #    Logger.debug("Normalizando Claves de Busqueda: {0}".format(key["entity"]))
            key_graph = graph_generator.build(key["entity"], levels=levels)
            neo4J = Neo4J()
            neo4J.save(key_graph)
            keys_entities.append({
                "entity": key["entity"],
                "graph": key_graph,
                "relevance": key["relevance"],
                "wiki": key["wiki"],
                "name": key["long_name"]
            })
        #Logger.debug("Normalizando Claves de Busqueda - Finalizado")

        return  keys_entities

    def get_graph(self, raw_graph):
        dic = {}
        from_g = []
        to_g = []
        for l, v in enumerate(raw_graph):
            dic.update(v)

        for key in dic.keys():

            from_g.append({"id": key})
            for l, v in enumerate(dic[key]):
                print(v)
                to_g.append({
                    "source": key,
                    "target": v.get("name"),
                    "level": v.get("level")
                })

        for m, t in enumerate(to_g):
            if(not self.inArr(t.get("target"), from_g)):
                from_g.append({"id":t.get("target")})

        return {
            "nodes": from_g,
            "links": to_g
        }

    def inArr(self, key, arr):
        #if not any(d.get('id', None) == key for d in arr):
        for f, g in enumerate(arr):
            if(key == g.get("id")):
                return  True

        return False

    def normalize_entities_by_key(self, url_entities = [], keys_entities = [], levels = 1):
        #Logger.debug("Normalizando Entidades por Engine")
        graph_generator = GraphGenerator()
        graph_generated = []
        for i, entity_by_engine in enumerate(url_entities):
            for k, entity in enumerate(entity_by_engine["entities"][0]):
                for j, key in enumerate(keys_entities):
                    key_graph = graph_generator.build(key["entity"], levels=levels)
                    graph_generated.append({
                        "entity": entity["entity"],
                        "relevance": entity["relevance"],
                        "wiki": entity["wiki"],
                        "graph": self.get_graph(key_graph),
                        "name": entity["long_name"],
                        "key": key
                    })
        #Logger.debug("Normalizando Entidades por Engine - Finalizado")

        return graph_generated

#test = GraphGenerator()
#prueba = {u'Simple_linear_regression': [{'relation': 1, 'name': u'Estimation_theory'}, {'relation': 1, 'name': u'Parametric_statistics'}, {'relation': 1, 'name': u'Regression_analysis'}]}, {u'Estimation_theory': [{'relation': 1, 'name': u'Estimation_theory'}, {'relation': 1, 'name': u'Signal_processing'}, {'relation': 1, 'name': u'Statistical_inference'}, {'relation': -1, 'name': u'Control_theory'}, {'relation': -1, 'name': u'Econometrics'}, {'relation': -1, 'name': u'Signal_processing'}, {'relation': -1, 'name': u'Statistical_theory'}, {'relation': -1, 'name': u'Telecommunication_theory'}]}, {u'Parametric_statistics': [{'relation': 1, 'name': u'Parametric_statistics'}, {'relation': 1, 'name': u'Statistical_inference'}, {'relation': -1, 'name': u'Hypothesis_testing'}]}, {u'Regression_analysis': [{'relation': 1, 'name': u'Actuarial_science'}, {'relation': 1, 'name': u'Estimation_theory'}, {'relation': 1, 'name': u'Regression_analysis'}, {'relation': 1, 'name': u'Statistical_methods'}, {'relation': -1, 'name': u'Estimation_theory'}, {'relation': -1, 'name': u'Mathematical_optimization'}, {'relation': -1, 'name': u'Multivariate_statistics'}, {'relation': -1, 'name': u'Statistical_models'}]}
#ml = "Machine_learning"
#res = test.get_ratio(prueba, ml)
#print(res)