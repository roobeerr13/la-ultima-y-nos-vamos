from neo4j import GraphDatabase

URI = "neo4j+s://d30f7b5d.databases.neo4j.io"
AUTH = ("neo4j", "J028d1qdxArBi0gO7bnk364fIMAzbBp77Wt0hLPc6-Y")

driver = GraphDatabase.driver(URI, auth=AUTH)