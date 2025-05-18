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