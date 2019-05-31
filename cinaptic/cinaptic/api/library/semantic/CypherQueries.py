from repository.Neo4J import *
from neomodel import db
import csv

class CypherQueries:
    def closeness_algo(self, nameGraph, relation, improved):
        query = f"""CALL algo.closeness.stream('MATCH (e:Entidad) WHERE e.idGraph="{nameGraph}" RETURN id(e) as id',
                        'MATCH (e1:Entidad)-[:{relation}]->(e2:Entidad) WHERE e1.idGraph="{nameGraph}" AND e2.idGraph="{nameGraph}" RETURN id(e1) as source, id(e2) as target',
                        {{graph:'cypher', write: true {", improved: true" if improved else ""} }})
                        YIELD nodeId, centrality
                        RETURN algo.getNodeById(nodeId).name as Entidad, centrality
                        ORDER BY centrality DESC
                        LIMIT 20;
                        """
        results, header = db.cypher_query(query)
        meta = f"Resultados algoritmo Closeness idGraph {nameGraph} relation {relation} improved {improved}"
        print(meta, results)
        self.exportCsv("_".join(meta.split(" ")), header, results)
        return results, header

    def closeness_harmonic_algo(self, nameGraph, relation):
        query = f"""CALL algo.closeness.harmonic.stream('MATCH (e:Entidad) WHERE e.idGraph="{nameGraph}" RETURN id(e) as id',
                        'MATCH (e1:Entidad)-[:{relation}]->(e2:Entidad) WHERE e1.idGraph="{nameGraph}" AND e2.idGraph="{nameGraph}" RETURN id(e1) as source, id(e2) as target',
                        {{graph:'cypher', write: true}})
                        YIELD nodeId, centrality
                        RETURN algo.getNodeById(nodeId).name as Entidad, centrality
                        ORDER BY centrality DESC
                        LIMIT 20;
                        """
        results, header = db.cypher_query(query)
        meta = f"Resultados algoritmo Harmonic Closeness idGraph {nameGraph} relation {relation}"
        print(meta, results)
        self.exportCsv("_".join(meta.split(" ")), header, results)
        return results, header

    def betweenness_algo(self, nameGraph, relation):
        query = f"""CALL algo.betweenness.stream('MATCH (e:Entidad) WHERE e.idGraph="{nameGraph}" RETURN id(e) as id',
                        'MATCH (e1:Entidad)-[:{relation}]->(e2:Entidad) WHERE e1.idGraph="{nameGraph}" AND e2.idGraph="{nameGraph}" RETURN id(e1) as source, id(e2) as target',
                        {{graph:'cypher', write: true}})
                        YIELD nodeId, centrality
                        RETURN algo.getNodeById(nodeId).name as Entidad, centrality
                        ORDER BY centrality DESC
                        LIMIT 20;
                        """
        results, header = db.cypher_query(query)
        meta = f"Resultados algoritmo Betweenness idGraph {nameGraph} relation {relation}"
        print(meta, results)
        self.exportCsv("_".join(meta.split(" ")), header, results)
        return results, header

    def pageRank_algo(self, nameGraph, relation, iterations, dampingFactor):
        query = f"""CALL algo.pageRank.stream('MATCH (e:Entidad) WHERE e.idGraph="{nameGraph}" RETURN id(e) as id',
                        'MATCH (e1:Entidad)-[:{relation}]->(e2:Entidad) WHERE e1.idGraph="{nameGraph}" AND e2.idGraph="{nameGraph}" RETURN id(e1) as source, id(e2) as target',
                        {{graph:'cypher', write: true, iterations:{iterations}, dampingFactor:{dampingFactor}}})
                        YIELD nodeId, score
                        RETURN algo.getNodeById(nodeId).name as Entidad, score
                        ORDER BY score DESC
                        LIMIT 20;
                        """
        results, header = db.cypher_query(query)
        meta = f"Resultados algoritmo PageRank idGraph {nameGraph} relation {relation} iterations {iterations} dampingFactor {dampingFactor}"
        print(meta, results)
        self.exportCsv("_".join(meta.split(" ")), header, results)
        return results, header

    def exportCsv(self, name, header, data):
        with open(name+'.csv', 'w') as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=',', lineterminator='\r\n')
            filewriter.writerow(header)
            filewriter.writerows(data)
        csvfile.close()