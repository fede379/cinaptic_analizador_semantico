from SPARQLWrapper import SPARQLWrapper, JSON
from consts import DBPEDIA_SPARKQL_ENDPOINT, \
    RESULTS, BINDINGS, VALUE, ARISTS_VALUE, NAME, \
    RELATION, SLASH_RESOURCE, TWO_POINTS
from repoze.lru import lru_cache

class DBPediaClient:

    def build_query(self, field, field_type, entity, with_category):
        query = """
                SELECT ?"""+field+"""
                WHERE { 
                    """+self.build_endpoint(entity, field_type , field, with_category) + """
                }
            """

        return query

    def build_query_is_broader_of(self, entity=""):
        query = """
                PREFIX  skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX  dbc:  <http://dbpedia.org/resource/Category:>
                PREFIX  dct:  <http://purl.org/dc/terms/>
                PREFIX  dbr: <http://dbpedia.org/resource/>
                
                SELECT  distinct ?is_of_relations
                WHERE
                  {   { SELECT  ?is_of_relations
                        WHERE   { ?is_of_relations dct:subject/skos:broader <http://dbpedia.org/resource/Category:"""+entity+"""> }
                      }
                        UNION
                      { SELECT  ?is_of_relations
                        WHERE { <http://dbpedia.org/resource/Category:"""+entity+"""> skos:broader  ?is_of_relations }
                      }
                      UNION
                      { SELECT  ?is_of_relations
                        WHERE { <http://dbpedia.org/resource/"""+entity+"""> dct:subject  ?is_of_relations 
                            FILTER( regex(str(?is_of_relations), "^(?!http://dbpedia.org/resource/Category:"""+entity+""")"))
                        }
                      }
                     
                  }
        """
        return query

    def build_endpoint(self, entity, field_type, field, with_category):
        default_endpoint = "<http://dbpedia.org/resource/{0}> {1} ?{2}".format(entity, field_type, field)
        if(with_category == True):
            default_endpoint = "<http://dbpedia.org/resource/Category:{0}> {1} ?{2}".format(entity, field_type, field)

        return default_endpoint



    @lru_cache(maxsize=50000)
    def get_entities(self, field="", field_type="", entity="", with_category=False, is_broader_flag=False, level=0):
        try:
            query = self.build_query_is_broader_of(entity=entity)

            sparql = SPARQLWrapper(DBPEDIA_SPARKQL_ENDPOINT)
            sparql.setQuery(query=query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            print(entity)
            return self.parse_entities(field=field, entities=results, is_broader_flag=is_broader_flag, level=level)
        except Exception, e:
            print(str(e))
            return []

    def parse_entities(self, field, entities, is_broader_flag, level):
        cs = []
        print("level: ",level + 1)
        for i, result in enumerate(entities[RESULTS][BINDINGS]):
            if(result[field][VALUE].find("/Category:") == -1):
                cs.append({
                    NAME: result[field][VALUE].split(SLASH_RESOURCE)[1],
                    RELATION: ARISTS_VALUE[field],
                    "level":level + 1
                })
            else:
                cs.append({
                        NAME: result[field][VALUE].split(TWO_POINTS)[2],
                        RELATION: ARISTS_VALUE[field],
                        "level": level + 1
                })

        return cs

    def new_query(self, entity, offset):
        query = """
            PREFIX  skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX  dbc:  <http://dbpedia.org/resource/Category:>
            PREFIX  dct:  <http://purl.org/dc/terms/>
            PREFIX  dbr:  <http://dbpedia.org/resource/>
            
            SELECT DISTINCT  *
            WHERE
              { ?level1  dct:subject  <http://dbpedia.org/resource/Category:"""+entity+"""> ;
                         dct:subject  ?level2 .
                ?level3  dct:subject  ?level2 ;
                         dct:subject  ?level4
                FILTER ( regex(str(?level2), "^(?!http://dbpedia.org/resource/Category"""+entity+""")") && 
                            regex(str(?level4), "^(?!http://dbpedia.org/resource/Category:"""+entity+""")")
                            && (?level3 != ?level1)  )
              }
            ORDER BY ASC(?level1)
            LIMIT 5000
            OFFSET """+offset+"""
        """