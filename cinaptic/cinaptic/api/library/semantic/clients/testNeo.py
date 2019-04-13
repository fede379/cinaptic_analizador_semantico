from neomodel import StructuredRel, StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config
config.DATABASE_URL = 'bolt://neo4j:cinaptic@localhost:11001'

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

from dbpediaClient import* 
client = DBPediaClient()
relations = client.gen_graph_for_neo("Pesticide_residue",5)
for r in relations:
    print r
    try:
        
            e1 = Entidad.nodes.get_or_none(name=r[0])
            if e1 is None:
                e1 = Entidad(name=r[0])
                e1.save()
            e2 = Entidad.nodes.get_or_none(name=r[2])
            if e2 is None:
                e2 = Entidad(name=r[2])
                e2.save()
            if r[1] == 'subject':
                rel = e1.subject.relationship(e2)
                if rel is None:
                    m = e2.subject.connect(e1)
                    m.save()
            if r[1] == 'broader':
                rel = e1.broader.relationship(e2)
                if rel is None:
                    m = e2.broader.connect(e1)
                    m.save()

    except Exception, e:
        print e
        pass

    
#
#class Entidad(StructuredNode):
#    title = StringProperty(unique_index=True)
#    entidad = RelationshipTo('Entidad', 'AUTHOR')
#
#class Author(StructuredNode):
#    name = StringProperty(unique_index=True)
#    books = RelationshipFrom('Book', 'AUTHOR')
#
#harry_potter = Book(title='Harry potter and the..').save()
#rowling =  Author(name='J. K. Rowling').save()
#harry_potter.author.connect(rowling)

