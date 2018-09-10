
class Analyser:

    def analyse(self, keys_enities, url_entities):
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
                    for i, ke in enumerate(keys_enities):
                        values.append({
                            "id": ke.get("entity"),
                            "value": self.exist_entity_in_graph(ke.get("graph"), ue.get("entity"), ke.get("entity"))
                        })
                    print(ue.get("relevance"))
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

    def exist_entity_in_graph(self, graph, entidad, key_entity):
        if(entidad == key_entity):
            return 0
        levels = [item["level"] for item in graph.get("links") if item["target"] == entidad]
        if(len(levels) > 0):
            return min(levels, key=float)
        else:
            return -1