from dbpediaClient import DBPediaClient
import pickle
import threading
key_words = ["Pesticide_residue", "Pesticide_treatment", "Residue_treatment" , "Pesticide_residue_treatment"]

def worker(key_word,levels):
	filename = str(key_word)+str(levels)
	data = client.gen_graph_for_neo_no_dirigido(key_word,levels)
	outfile = open(filename,'wb')
	pickle.dump(data,outfile)
	outfile.close()
	return data

threads = list()
for key_word in key_words:
    t = threading.Thread(target=worker, args=(key_word,levels,))
    threads.append(t)
    t.start()

#para abrir:
# infile = open(filename,'rb')
# data= pickle.load(infile)
# print(data)
# infile.close()