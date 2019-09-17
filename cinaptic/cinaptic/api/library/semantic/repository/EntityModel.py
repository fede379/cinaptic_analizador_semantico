from neomodel import StructuredRel, StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config
#config.DATABASE_URL = 'bolt://neo4j:Pesticide@localhost:11004'
config.DATABASE_URL = 'bolt://neo4j:cinaptic@localhost:7687'    #local url
# config.DATABASE_URL = 'bolt://neo4j:cinaptic@10.13.0.146:7687'    #server url
#config.DATABASE_URL = 'bolt://neo4j:Pesticide_treatment@localhost:11001'
#config.DATABASE_URL = 'bolt://neo4j:Treatment@localhost:11001'
#config.DATABASE_URL = 'bolt://neo4j:Residue_treatment@localhost:11001'
#config.DATABASE_URL = 'bolt://neo4j:Pesticide_residue_treatment@localhost:11001'

class Relation(StructuredRel):
    name = StringProperty()

class Entidad(StructuredNode):
    name = StringProperty(unique_index=True)
    relation = RelationshipTo('Entidad', 'Relation', model=Relation )