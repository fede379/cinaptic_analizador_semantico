self.p.MERGE.node('e', 'Entidad', name='Water', relevance=0,7, idGraph='nombre_grafo')  
self.p.MERGE.node('e', 'Entidad', name='Water_quality', relevance=0,7, idGraph='nombre_grafo')   
self.p.MATCH.node('e1', 'Entidad', name='Water', idGraph= 'nombre_grafo').node('e2', 'Entidad', name='Water_quality', idGraph='nombre_grafo').CREATE.node(e1).rel_out(labels='RELATION').node(e2)


MATCH (e)-[r]-() DELETE e,r

// BETWEENESS ALGO
CALL algo.betweenness.stream('MATCH (e:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e) as id',
'MATCH (e1:Entidad{idGraph:"Risotto-Paella"})-[:RELATION]-(e2:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e1) as source, id(e2) as target',
{graph:'cypher'})
YIELD nodeId, centrality
RETURN algo.getNodeById(nodeId).name as Entidad, centrality
ORDER BY centrality DESC
LIMIT 50;

// CLOSENESS ALGO
CALL algo.closeness.stream('MATCH (e:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e) as id',
'MATCH (e1:Entidad{idGraph:"Risotto-Paella"})-[:RELATION]-(e2:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e1) as source, id(e2) as target',
{graph:'cypher'})
YIELD nodeId, centrality
RETURN algo.getNodeById(nodeId).name as Entidad, centrality
ORDER BY centrality DESC
LIMIT 50;

// DEGREE ALGO outgoing
CALL algo.degree.stream('MATCH (e:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e) as id',
'MATCH (e1:Entidad{idGraph:"Risotto-Paella"})-[r:RELATION]->(e2:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e1) as source, id(e2) as target, r.relevance as weight', {graph:'cypher', weightProperty: 'weight'})
YIELD nodeId, score
RETURN algo.asNode(nodeId).name AS Entidad, score
ORDER BY score DESC
LIMIT 50;

// degree incoming
CALL algo.degree.stream('MATCH (e:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e) as id',
'MATCH (e1:Entidad{idGraph:"Risotto-Paella"})<-[r:RELATION]-(e2:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e1) as source, id(e2) as target, r.relevance as weight', {graph:'cypher', weightProperty: 'weight'})
YIELD nodeId, score
RETURN algo.asNode(nodeId).name AS Entidad, score
ORDER BY score DESC
LIMIT 50;

// eigenvector algo
CALL algo.eigenvector.stream('MATCH (e:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e) as id',
'MATCH (e1:Entidad{idGraph:"Risotto-Paella"})-[r:RELATION]-(e2:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e1) as source, id(e2) as target', {graph: 'cypher', normalization: 'max'})
YIELD nodeId, score
RETURN algo.asNode(nodeId).name AS Entidad, score
ORDER BY score DESC
LIMIT 50;

// closeness harmonic algo
CALL algo.closeness.harmonic.stream('MATCH (e:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e) as id',
'MATCH (e1:Entidad{idGraph:"Risotto-Paella"})-[:RELATION]-(e2:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e1) as source, id(e2) as target',
{graph:'cypher'})
YIELD nodeId, centrality
RETURN algo.getNodeById(nodeId).name as Entidad, centrality
ORDER BY centrality DESC
LIMIT 50;

// PageRank algo
CALL algo.pageRank.stream('MATCH (e:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e) as id',
'MATCH (e1:Entidad{idGraph:"Risotto-Paella"})-[r:RELATION]-(e2:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e1) as source, id(e2) as target, r.relevance as weight', {graph: 'cypher', iterations:20, dampingFactor:0.85, weightProperty: "weight"})
YIELD nodeId, score
RETURN algo.asNode(nodeId).name AS Entidad, score
ORDER BY score DESC
LIMIT 50;

// count traingles clustering algo
CALL algo.triangleCount.stream('MATCH (e:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e) as id',
'MATCH (e1:Entidad{idGraph:"Risotto-Paella"})-[:RELATION]-(e2:Entidad{idGraph:"Risotto-Paella"}) RETURN id(e1) as source, id(e2) as target',
{graph:'cypher'})
YIELD nodeId, triangles, coefficient
RETURN algo.getNodeById(nodeId).name as Entidad, triangles, coefficient
ORDER BY triangles DESC
LIMIT 50;