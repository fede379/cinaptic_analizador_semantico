from dbpediaClient import DBPediaClient
client = DBPediaClient()

for relation in (client.gen_graph_for_neo_no_dirigido("Machine_learning",2)):
	print(relation)