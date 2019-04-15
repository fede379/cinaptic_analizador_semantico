from neomodel import StructuredRel, StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config
#config.DATABASE_URL = 'bolt://neo4j:Pesticide@localhost:11004'
config.DATABASE_URL = 'bolt://neo4j:cinaptic@localhost:11007'
#config.DATABASE_URL = 'bolt://neo4j:Pesticide_treatment@localhost:11001'
#config.DATABASE_URL = 'bolt://neo4j:Treatment@localhost:11001'
#config.DATABASE_URL = 'bolt://neo4j:Residue_treatment@localhost:11001'
#config.DATABASE_URL = 'bolt://neo4j:Pesticide_residue_treatment@localhost:11001'

class SubjectRel(StructuredRel):
    rel = StringProperty()

class IsSubjectRel(StructuredRel):
    rel = StringProperty()

class BroaderRel(StructuredRel):
    rel = StringProperty()

class isBroaderRel(StructuredRel):
    rel = StringProperty()

class Entidad(StructuredNode):
    name = StringProperty(unique_index=True)
    subject = RelationshipTo('Entidad', 'SUBJECT', model=SubjectRel)
    is_subject_of = RelationshipTo('Entidad', 'IS_SUBJECT_OF', model=IsSubjectRel)
    broader = RelationshipTo('Entidad', 'BROADER', model=BroaderRel)
    is_broader_of = RelationshipTo('Entidad', 'IS_BROADER_OF', model=isBroaderRel)
