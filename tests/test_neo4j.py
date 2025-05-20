from neo4j import GraphDatabase

URI = "neo4j+s://<TU_URL_DE_AURA>"
USER = "neo4j"
PASSWORD = "<TU_CONTRASEÑA>"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def test_connection(tx):
    result = tx.run("RETURN 'Conexión exitosa' AS message")
    for record in result:
        print(record["message"])

with driver.session() as session:
    session.execute_write(test_connection)

driver.close()



from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+s://d30f7b5d.databases.neo4j.io"
AUTH = ("neo4j", "J028d1qdxArBi0gO7bnk364fIMAzbBp77Wt0hLPc6-Y")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()