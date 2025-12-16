#Author: Abhisekhar Bharadwaj Gandavarapu
#ASU ID: 1219773724


from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, last_node):
        with self._driver.session() as session:
            result = session.run("""
                MATCH (start:Location {name: $start_node}), (end:Location {name: $last_node})
                MATCH path = shortestPath((start)-[:TRIP*]->(end))
                RETURN [node IN nodes(path) | {name: node.name}] AS path
            """, start_node=start_node, last_node=last_node)
            
            record = result.single()
            if record:
                return [{'path': record['path']}]
            else:
                return []

    def pagerank(self, max_iterations, weight_property):
        with self._driver.session() as session:
            try:
                session.run("CALL gds.graph.drop('pagerank-graph', false)")
            except:
                pass
            
            session.run("""
                CALL gds.graph.project(
                    'pagerank-graph',
                    'Location',
                    'TRIP',
                    {
                        relationshipProperties: $weight_property
                    }
                )
            """, weight_property=weight_property)
            
            result = session.run("""
                CALL gds.pageRank.stream('pagerank-graph', {
                    maxIterations: $max_iterations,
                    relationshipWeightProperty: $weight_property
                })
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name AS name, score
                ORDER BY score DESC
            """, max_iterations=max_iterations, weight_property=weight_property)
            
            all_results = list(result)
            session.run("CALL gds.graph.drop('pagerank-graph', false)")
            
            max_node = {'name': all_results[0]['name'], 'score': all_results[0]['score']}
            min_node = {'name': all_results[-1]['name'], 'score': all_results[-1]['score']}
            
            return [max_node, min_node]

