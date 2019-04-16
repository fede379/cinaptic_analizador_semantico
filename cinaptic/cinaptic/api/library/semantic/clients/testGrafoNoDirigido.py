from dbpediaClient import DBPediaClient
import pickle

client = DBPediaClient()
file_name = "Pesticide_residue_5_levels"
data = client.gen_graph_for_neo_no_dirigido("Pesticide_residue",5)
outfile = open(filename,'wb')
pickle.dump(data,outfile)
outfile.close()
#para abrir:

infile = open(filename,'rb')
data= pickle.load(infile)
infile.close()