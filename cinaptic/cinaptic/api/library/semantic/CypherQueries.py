from .repository.Neo4J import *
from neomodel import db
import csv
import logging
import os

logger = logging.getLogger()

class CypherQueries:
    def closeness_algo(self, nameGraph, relation, improved):
        query = f'''CALL algo.closeness.stream('MATCH (e:Entidad) WHERE e.idGraph=\"{nameGraph}\" RETURN id(e) as id',
                    'MATCH (e1:Entidad)-[:{relation}]->(e2:Entidad) WHERE e1.idGraph=\"{nameGraph}\" AND e2.idGraph=\"{nameGraph}\" RETURN id(e1) as source, id(e2) as target',
                    {{graph:'cypher', write: true {', improved: true' if improved else ""} }})
                    YIELD nodeId, centrality
                    RETURN algo.getNodeById(nodeId).name as Entidad, centrality
                    ORDER BY centrality DESC
                    LIMIT 50;'''                    
        results, header = db.cypher_query(query)
        meta = f"Closeness idGraph {nameGraph} relation {relation} improved {improved}"
        #print(meta, results)
        path = self.exportCsv("_".join(meta.split(" ")), header, results, nameGraph)
        logger.info(meta + " saved in " + path)
        return path

    def closeness_harmonic_algo(self, nameGraph, relation):
        query = f'''CALL algo.closeness.harmonic.stream('MATCH (e:Entidad) WHERE e.idGraph=\"{nameGraph}\" RETURN id(e) as id',
                    'MATCH (e1:Entidad)-[:{relation}]->(e2:Entidad) WHERE e1.idGraph=\"{nameGraph}\" AND e2.idGraph=\"{nameGraph}\" RETURN id(e1) as source, id(e2) as target',
                    {{graph:'cypher', write: true}})
                    YIELD nodeId, centrality
                    RETURN algo.getNodeById(nodeId).name as Entidad, centrality
                    ORDER BY centrality DESC
                    LIMIT 50;'''
        results, header = db.cypher_query(query)
        meta = f"Harmonic Closeness idGraph {nameGraph} relation {relation}"
        #print(meta, results)
        path = self.exportCsv("_".join(meta.split(" ")), header, results, nameGraph)
        logger.info(meta + " saved in " + path)
        return path

    def betweenness_algo(self, nameGraph, relation):
        query = f'''CALL algo.betweenness.stream('MATCH (e:Entidad) WHERE e.idGraph=\"{nameGraph}\" RETURN id(e) as id',
                    'MATCH (e1:Entidad)-[:{relation}]->(e2:Entidad) WHERE e1.idGraph=\"{nameGraph}\" AND e2.idGraph=\"{nameGraph}\" RETURN id(e1) as source, id(e2) as target',
                    {{graph:'cypher', write: true}})
                    YIELD nodeId, centrality
                    RETURN algo.getNodeById(nodeId).name as Entidad, centrality
                    ORDER BY centrality DESC
                    LIMIT 50;'''
        results, header = db.cypher_query(query)
        meta = f"Betweenness idGraph {nameGraph} relation {relation}"
        #print(meta, results)
        logger.info(meta)
        path = self.exportCsv("_".join(meta.split(" ")), header, results, nameGraph)
        return path

    def pageRank_algo(self, nameGraph, relation, iterations, dampingFactor):
        query = f'''CALL algo.pageRank.stream('MATCH (e:Entidad) WHERE e.idGraph=\"{nameGraph}\" RETURN id(e) as id',
                    'MATCH (e1:Entidad)-[:{relation}]->(e2:Entidad) WHERE e1.idGraph=\"{nameGraph}\" AND e2.idGraph=\"{nameGraph}\" RETURN id(e1) as source, id(e2) as target',
                    {{graph:'cypher', write: true, iterations:{iterations}, dampingFactor:{dampingFactor}}})
                    YIELD nodeId, score
                    RETURN algo.getNodeById(nodeId).name as Entidad, score
                    ORDER BY score DESC
                    LIMIT 50;'''
        results, header = db.cypher_query(query)
        meta = f"PageRank idGraph {nameGraph} relation {relation} iterations {iterations} dampingFactor {dampingFactor}"
        #print(meta, results)
        path = self.exportCsv("_".join(meta.split(" ")), header, results, nameGraph)
        logger.info(meta + " saved in " + path)
        return path

    def degree_algo(self, nameGraph, relation, direction):
        if (direction == "incoming" or direction == "outcoming"):
            query = f'''CALL algo.degree.stream('MATCH (e:Entidad) WHERE e.idGraph=\"{nameGraph}\" RETURN id(e) as id',
                        'MATCH (e1:Entidad){'<-' if (direction=="incoming") else "-"}[:{relation}]{'->' if (direction=="outcoming") else "-"}(e2:Entidad) WHERE e1.idGraph=\"{nameGraph}\" AND e2.idGraph=\"{nameGraph}\" RETURN id(e1) as source, id(e2) as target', {{graph:'cypher'}})
                        YIELD nodeId, score
                        RETURN algo.asNode(nodeId).name AS name, score
                        ORDER BY score DESC
                        LIMIT 50;'''
            results, header = db.cypher_query(query)
            meta = f"Degree idGraph {nameGraph} relation {relation} direction {direction}"
            #print(meta, results)
            path = self.exportCsv("_".join(meta.split(" ")), header, results, nameGraph)
            logger.info(meta + " saved in " + path)
            return path
        return None

    def exportCsv(self, name, header, data, nameGraph):
        path = f"results/{nameGraph}"
        if not os.path.exists(path):
            os.mkdir(path)
        path = f"{path}/{name}.csv"
        with open(path, 'w') as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=',', lineterminator='\r\n')
            filewriter.writerow(header)
            filewriter.writerows(data)
        csvfile.close()
        return path
