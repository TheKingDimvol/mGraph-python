from neo4j import GraphDatabase


DRIVER = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "mGraph"))
