from repository.Neo4J import *
from neomodel import db
class Analyser:

    def analyse(self, keys_entities, url_entities):
        result = []
        for i, engine in enumerate(url_entities):
            engines = []
            urls_info = []
            for j, urls in enumerate(engine.get("results")):
                url_info = {
                    "url":urls.get("url"),
                }
                table_x_url = []
                for k, ue in enumerate(urls.get("entities")):
                    values = []
                    for i, ke in enumerate(keys_entities):
                        values.append({
                            "id": ke.get("entity"),
                            "value": self.exist_entity_in_graph(ue.get("entity"), ke.get("entity"))
                        })
                    m = {
                        "entidad":ue.get("entity"),
                        "relevance":ue.get("relevance")
                    }
                    for v, value in enumerate(values):
                        m.update({
                            value.get("id"):value.get("value")
                        })

                    table_x_url.append(m)
                url_info["table"] = table_x_url
                urls_info.append(url_info)
            engines.append({
                "engine":engine.get("engine"),
                "urls":urls_info
            })

            result.append(engines)


        return result

    def exist_entity_in_graph(self, entidad, key_entity):
        if(entidad == key_entity):
            return 0
        e1 = Entidad.nodes.get_or_none(name=key_entity)
        e2 = Entidad.nodes.get_or_none(name=entidad)
        if(e1 is None or e2 is None):
            print("e1 or e2 does not exists")
            return -1
        try:
            query = """
                    MATCH   (e1:Entidad {{ name: "{e_one}" }}), 
                        (e2:Entidad {{ name: "{e_two}" }}),
                        p = shortestPath((e1)-[*..15]-(e2))
                RETURN length(p) + 1
                """.format(e_one=key_entity,e_two=entidad)
            results, _ = db.cypher_query(query)
            return results[0][0]
        except:
            return -2
            
