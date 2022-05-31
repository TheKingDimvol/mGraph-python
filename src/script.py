if __name__ == '__main__':
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver("bolt://176.57.217.75:7687", auth=("neo4j", "miner2"))
    with driver.session() as session:
        a = """
            MATCH (node)<-[{type: 'СОДЕРЖИТ'}]-(:Доска)-[*0..{type: 'ИСПОЛЬЗУЕТ'}]->(desk:Доска)-[*0..{type: 'ИСПОЛЬЗУЕТ'}]->(typology:Типология)
            RETURN ID(desk) AS id, LABELS(desk) AS labels, desk AS params, typology.uuid, typology.title, count(DISTINCT node) AS nodes
        """
        result = session.run("""
            MATCH (n)
            return distinct labels(n)
        """)
        data = result.data()
        for record in data:
            a = record
