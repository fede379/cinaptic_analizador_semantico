from dbpediaClient import DBPediaClient
import pickle

key_words = ["Pesticide_residue", "Pesticide_treatment", "Residue_treatment" , "Pesticide_residue_treatment"]
for key_word in key_words:
	levels = 5
	client = DBPediaClient()
	filename = str(key_word)+str(levels)
	data = client.gen_graph_for_neo_no_dirigido(key_word,levels)
	outfile = open(filename,'wb')
	pickle.dump(data,outfile)
	outfile.close()

#para abrir:
# infile = open(filename,'rb')
# data= pickle.load(infile)
# print(data)
# infile.close()