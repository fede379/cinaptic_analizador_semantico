self.p.MERGE.node('e', 'Entidad', name='Water', relevance=0,7, idGraph='nombre_grafo')  
self.p.MERGE.node('e', 'Entidad', name='Water_quality', relevance=0,7, idGraph='nombre_grafo')   
self.p.MATCH.node('e1', 'Entidad', name='Water', idGraph= 'nombre_grafo').node('e2', 'Entidad', name='Water_quality', idGraph='nombre_grafo').CREATE.node(e1).rel_out(labels='RELATION').node(e2)