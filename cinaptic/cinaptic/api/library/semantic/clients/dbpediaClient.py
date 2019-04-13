from SPARQLWrapper import SPARQLWrapper, JSON
from consts import DBPEDIA_SPARKQL_ENDPOINT, \
    RESULTS, BINDINGS, VALUE, ARISTS_VALUE, NAME, \
    RELATION, SLASH_RESOURCE, TWO_POINTS

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



    #@lru_cache(maxsize=50000)
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

    def gen_graph_for_neo(self,entity,niveles):
        #explicacion: https://drive.google.com/file/d/12AkYQJjNaywTnrBSXWBAYTKefF9Letj8/view?usp=sharing
        dct_relations = get_dct_subject_relations(entity,niveles)
        dc_relations = get_dc_subject_relations(entity,niveles)
        skos_relations = get_skos_broader_relations(entity,niveles)
        mixed_relations = get_mixed_relations(entity,niveles)

        relations = []
        for r in dct_relations:
            relations.append(r)
        for r in dc_relations:
            relations.append(r)
        for r in skos_relations:
            relations.append(r)
        for r in mixed_relations:
            relations.append(r)

        relations = set(relations)
        #se eliminan los duplicados mediante el uso del conjunto
        relations = list(relations)
        how_many_relations = 0
        for r in relations:
            how_many_relations = how_many_relations + 1
            print(r)
        print ("cantidad de relaciones: "+str(how_many_relations))
        return relations

def get_dct_subject_relations(entity,niveles):
    relations = []
    sparql = SPARQLWrapper(DBPEDIA_SPARKQL_ENDPOINT)
    #entity como category
    #las entidades devueltas son resources
    query_dct = get_prefixes() + """SELECT DISTINCT  ?entity
                WHERE
                    {
                        ?entity dct:subject <http://dbpedia.org/resource/Category:"""+entity+"""> .
                    }
                """
    
    sparql.setQuery(query=query_dct)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if len(results["results"]["bindings"])>0:
        for json_entity in results["results"]["bindings"]:
            #http://dbpedia.org/resource/Learning
            e =json_entity["entity"]["value"].split("/")[4]
            relations.append((e,"subject",entity))
    #entity como resource
    #las entidades devueltas son categories
    query_dct = get_prefixes() + """SELECT DISTINCT  ?entity
                WHERE
                    {
                        <http://dbpedia.org/resource/"""+entity+"""> dct:subject ?entity .
                    }
                """

    sparql.setQuery(query=query_dct)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if len(results["results"]["bindings"])>0:
        for json_entity in results["results"]["bindings"]:
            #http://dbpedia.org/resource/Category:Learning
            e =json_entity["entity"]["value"].split(":")[2]
            relations.append((entity,"subject",e))
    return set(relations)

def get_dc_subject_relations(entity,niveles):
    relations = []
    sparql = SPARQLWrapper(DBPEDIA_SPARKQL_ENDPOINT)
    if niveles >= 1:
        query_dc = """
                PREFIX  dbc:  <http://dbpedia.org/resource/Category:>
                PREFIX  dc:  <http://purl.org/dc/elements/1.1/>
                PREFIX  dbr:  <http://dbpedia.org/resource/>
                
                SELECT DISTINCT  ?entity
                WHERE
                    {
                        ?entity dc:subject <http://dbpedia.org/resource/"""+entity+"""> .
                    }
                """
        sparql.setQuery(query=query_dc)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                e =json_entity["entity"]["value"].split("/")[4]
                relations.append((e,"subject",entity))

        query_dc =  """
                        PREFIX  dbc:  <http://dbpedia.org/resource/Category:>
                        PREFIX  dc:  <http://purl.org/dc/elements/1.1/>
                        PREFIX  dbr:  <http://dbpedia.org/resource/>
                        
                        SELECT DISTINCT  ?entity
                        WHERE
                            {
                                <http://dbpedia.org/resource/"""+entity+"""> dc:subject ?entity .
                            }
                    """
        sparql.setQuery(query=query_dc)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                e =json_entity["entity"]["value"].split("/")[4]
                relations.append((entity,"subject",e))
    if niveles >= 2:
        query_dc =  """
                        PREFIX  dbc:  <http://dbpedia.org/resource/Category:>
                        PREFIX  dc:  <http://purl.org/dc/elements/1.1/>
                        PREFIX  dbr:  <http://dbpedia.org/resource/>
                        
                        SELECT DISTINCT  ?entity1 ?entity2
                        WHERE
                            {
                                ?entity1 dc:subject ?entity2 .
                                ?entity2 dc:subject <http://dbpedia.org/resource/"""+entity+"""> .
                            }
                    """
        sparql.setQuery(query=query_dc)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                e1 =json_entity["entity1"]["value"].split("/")[4]
                e2 =json_entity["entity2"]["value"].split("/")[4]
                relations.append((e1,"subject",e2))
                relations.append((e2,"subject",entity))

        query_dc =  """
                    PREFIX  dbc:  <http://dbpedia.org/resource/Category:>
                    PREFIX  dc:  <http://purl.org/dc/elements/1.1/>
                    PREFIX  dbr:  <http://dbpedia.org/resource/>
                    
                    SELECT DISTINCT  ?entity1 ?entity2
                    WHERE
                        {
                            <http://dbpedia.org/resource/"""+entity+"""> dc:subject ?entity1 .
                            ?entity1 dc:subject ?entity2 
                        }
                    """ 
        sparql.setQuery(query=query_dc)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                e1 =json_entity["entity1"]["value"].split("/")[4]
                e2 =json_entity["entity2"]["value"].split("/")[4]
                relations.append((entity,"subject",e1))
                relations.append((e1,"subject",e2))
    return set(relations)

def get_skos_broader_relations(entity,niveles):
    relations = []
    sparql = SPARQLWrapper(DBPEDIA_SPARKQL_ENDPOINT)

    for nivel in range(1,niveles):
        query_skos =    get_prefixes() + select_clause_generator(nivel)+"""
                            WHERE
                                {
                                    """+where_clause_generator(nivel)+"""
                                    ?entity"""+str(nivel)+""" skos:broader <http://dbpedia.org/resource/Category:"""+entity+""">  .
                                    
                                }
                        """
        sparql.setQuery(query=query_skos)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                
                for i in range(1,nivel):
                    entity1 = "entity"+str(i)
                    entity2 = "entity"+str(i+1)
                    e1 =json_entity[entity1]["value"].split(":")[2]
                    e2 =json_entity[entity2]["value"].split(":")[2]
                    relations.append((e1,"subject",e2))
                entity2 = "entity"+str(nivel)
                e2 =json_entity[entity2]["value"].split(":")[2]
                relations.append((e2,"broader",entity))
                
    for nivel in range(1,niveles):
        query_skos =    get_prefixes() +select_clause_generator(nivel)+"""
                            WHERE
                                {
                                    <http://dbpedia.org/resource/Category:"""+entity+"""> skos:broader ?entity"""+str(1)+""" .
                                    """+where_clause_generator(nivel)+"""
                                    
                                }
                        """ 
        sparql.setQuery(query=query_skos)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                entity1 = "entity"+str(1)
                e1 =json_entity[entity1]["value"].split(":")[2]
                relations.append((entity,"subject",e1))   
                for i in range(1,nivel):
                    entity1 = "entity"+str(i)
                    entity2 = "entity"+str(i+1)
                    e1 =json_entity[entity1]["value"].split(":")[2]
                    e2 =json_entity[entity2]["value"].split(":")[2]
                    relations.append((e1,"broader",e2))
    return set(relations)

def get_prefixes():
    prefixes =  """
                PREFIX  dbc:  <http://dbpedia.org/resource/Category:>
                PREFIX  dct:  <http://purl.org/dc/terms/>
                PREFIX  dbr:  <http://dbpedia.org/resource/>
                PREFIX  skos: <http://www.w3.org/2004/02/skos/core#>
                """
    return prefixes

def select_clause_generator(nivel):
    s = " SELECT DISTINCT "
    for i in range(1, nivel+1):
        s = s + " ?entity"+str(i)
    return s
def where_clause_generator(nivel):
    s = ""
    for i in range(1, nivel):
        s = s + " ?entity"+str(i) + " skos:broader " + " ?entity"+str(i+1) + " .\n"
    return s

def get_mixed_relations(entity, niveles):
    relations = []
    sparql = SPARQLWrapper(DBPEDIA_SPARKQL_ENDPOINT)
    #en princio mezclar relaciones tiene sentidod si tenemos al menos dos saltos, es decir, 3 niveles
    if niveles > 2: #niveles = 3 
    #case 01
        query = get_prefixes()+"""SELECT DISTINCT ?entity1 ?entity2 WHERE
        {
            <http://dbpedia.org/resource/"""+entity+""">  dct:subject ?entity1.
            ?entity1 skos:broader ?entity2.
        }"""
        sparql.setQuery(query=query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                e1 =json_entity["entity1"]["value"].split(":")[2]
                e2 =json_entity["entity2"]["value"].split(":")[2]
                relations.append((entity,"subject",e1))
                relations.append((e1,"broader",e2))
    #case 02
        query = get_prefixes()+"""SELECT DISTINCT ?entity1 ?entity2 WHERE
        {
            ?entity1 dc:subject ?entity2 . 
            ?entity2 dct:subject <http://dbpedia.org/resource/Category:"""+entity+""">  .
            
        }"""
        sparql.setQuery(query=query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                e1 =json_entity["entity1"]["value"].split("/")[4]
                e2 =json_entity["entity2"]["value"].split("/")[4]
                relations.append((e1,"subject",e2))
                relations.append((e2,"subject",entity))
    #case 03
        query = get_prefixes()+"""SELECT DISTINCT ?entity1 ?entity2 WHERE
        {
            ?entity1 dct:subject ?entity2 . 
            ?entity2 skos:broader <http://dbpedia.org/resource/Category:"""+entity+""">  .
            
        }"""
        sparql.setQuery(query=query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                e1 =json_entity["entity1"]["value"].split("/")[4]
                e2 =json_entity["entity2"]["value"].split(":")[2]
                relations.append((e1,"subject",e2))
                relations.append((e2,"broader",entity))
    if niveles > 3:
        #caso01
        query = get_prefixes()+ select_clause_generator(niveles-1)+""" WHERE
        {   
            <http://dbpedia.org/resource/"""+entity+"""> dct:subject ?entity1 . 
            """+gen_n_relations(niveles-2,from_entity_number=1,relation="skos:broader")+"""
              
        }"""
        sparql.setQuery(query=query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                entity1 = "entity"+str(1)
                e1 =json_entity[entity1]["value"].split(":")[2]
                relations.append((entity,"subject",e1))   
                for i in range(1,niveles-1):
                    entity1 = "entity"+str(i)
                    entity2 = "entity"+str(i+1)
                    e1 =json_entity[entity1]["value"].split(":")[2]
                    e2 =json_entity[entity2]["value"].split(":")[2]
                    relations.append((e1,"broader",e2))
        #case 02
        for n in range (1,niveles):
            query = get_prefixes()+ select_clause_generator(niveles-1)+""" WHERE
            {
                <http://dbpedia.org/resource/"""+entity+"""> dc:subject ?entity1 . 
                """+gen_n_relations(n-1,from_entity_number=1,relation="dc:subject")+"""
                """+ gen_n_relations(1,from_entity_number=n-1,relation="dct:subject")+"""
                """+gen_n_relations(niveles-1-n,from_entity_number=n,relation="skos:broader")+"""
                
            }"""
            sparql.setQuery(query=query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            if len(results["results"]["bindings"])>0:
                for json_entity in results["results"]["bindings"]:
                    #http://dbpedia.org/resource/Learning
                    entity1 = "entity"+str(1)
                    e1 =json_entity[entity1]["value"].split("/")[4]
                    relations.append((entity,"subject",e1))   
                    for n in range(1,niveles-1):
                        for i in range(1,n+1):
                            entity1 = "entity"+str(i)
                            entity2 = "entity"+str(i+1)
                            e1 =json_entity[entity1]["value"].split("/")[4]
                            e2 =json_entity[entity2]["value"].split("/")[4]
                        relations.append((e1,"subject",e2))
                        for i in range(n,niveles):
                            entity1 = "entity"+str(i)
                            entity2 = "entity"+str(i+1)
                            e1 =json_entity[entity1]["value"].split(":")[2]
                            e2 =json_entity[entity2]["value"].split(":")[2]
                        relations.append((e1,"broader",e2))
        #caso03
        query = get_prefixes()+ select_clause_generator(niveles-1)+""" WHERE
        {
            """+gen_n_relations(niveles-1,from_entity_number=1,relation="dc:subject")+"""
              ?entity"""+str(niveles-1)+""" dct:subject <http://dbpedia.org/resource/Category:"""+entity+""">.
        }"""
        sparql.setQuery(query=query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"])>0:
            for json_entity in results["results"]["bindings"]:
                #http://dbpedia.org/resource/Learning
                
                for i in range(1,niveles-1):
                    entity1 = "entity"+str(i)
                    entity2 = "entity"+str(i+1)
                    e1 =json_entity[entity1]["value"].split("/")[4]
                    e2 =json_entity[entity2]["value"].split("/")[4]
                    relations.append((e1,"subject",e2))
                entity2 = "entity"+str(niveles-1)
                e2 =json_entity[entity2]["value"].split("/")[4]
                relations.append((e2,"broader",entity))
        
        #caso04
        for n in range(1,niveles):
            query = get_prefixes()+ select_clause_generator(niveles-1)+""" WHERE
            {
                """+gen_n_relations(n-1,from_entity_number=1,relation="dc:subject")+"""
                """+ gen_n_relations(1,from_entity_number=n-1,relation="dct:subject")+"""
                """+gen_n_relations(niveles-1-n,from_entity_number=n+1,relation="skos:broader")+"""
                  ?entity"""+str(niveles-1)+""" skos:broader <http://dbpedia.org/resource/Category:"""+entity+""">.
            }"""
            sparql.setQuery(query=query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            if len(results["results"]["bindings"])>0:
                for json_entity in results["results"]["bindings"]:
                    #http://dbpedia.org/resource/Learning
                    for n in range(1,niveles-1):
                        for i in range(1,n+1):
                            entity1 = "entity"+str(i)
                            entity2 = "entity"+str(i+1)
                            e1 =json_entity[entity1]["value"].split(":")[2]
                            e2 =json_entity[entity2]["value"].split(":")[2]
                        relations.append((e1,"subject",e2))
                        for i in range(n,niveles-1):
                            entity1 = "entity"+str(i)
                            entity2 = "entity"+str(i+1)
                            e1 =json_entity[entity1]["value"].split("/")[4]
                            e2 =json_entity[entity2]["value"].split("/")[4]
                        relations.append((e1,"broader",e2))
                    entity2 = "entity"+str(niveles-1)
                    e2 =json_entity[entity2]["value"].split("/")[4]
                    relations.append((e2,"broader",entity))
    return relations

def gen_n_relations(n,from_entity_number,relation):
    s = ""
    for i in range (from_entity_number,n+from_entity_number):
        s = s + "?entity"+str(i)+" "+str(relation)+" "+"?entity"+str(i+1) + " . \n"
    return s


        



            


            


