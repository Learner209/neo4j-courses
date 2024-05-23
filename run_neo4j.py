import argparse
from neo4j import GraphDatabase, exceptions


def is_valid_cypher_query(line):
    # List of typical starting keywords for Cypher queries
    valid_keywords = ["CREATE", "MATCH", "MERGE", "RETURN", "WITH", "SET", "DELETE", "REMOVE", "UNWIND", "CALL"]
    return any(line.strip().startswith(keyword) for keyword in valid_keywords)


class Neo4jConnection:
    def __init__(self, uri, user, pwd, db):
        self.__uri = uri
        self.__user = user
        self.__password = pwd
        self.__driver = None
        self.__db = db
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__password))
            # self.create_database_if_not_exists() # for now, community edition doesn't support CREATE DATABASE IF NOT EXISTS
        except Exception as e:
            print("Failed to create the driver:", e)
        self.clear_database()

    def close(self):
        if self.__driver:
            self.__driver.close()

    def clear_database(self):
        with self.__driver.session(database=self.__db) as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("All nodes and relationships have been deleted.")

    def create_database_if_not_exists(self):
        try:
            with self.__driver.session() as session:
                session.run(f"CREATE DATABASE {self.__db} IF NOT EXISTS")
        except exceptions.ClientError as e:
            if "UnsupportedAdministrationCommand" in e.message:
                print(f"Database '{self.__db}' already exists or cannot be created via this method.")
            else:
                raise

    def query(self, query, parameters=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=self.__db)
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


# Argument Parser Setup
parser = argparse.ArgumentParser(description="Run Cypher queries in Neo4j")
parser.add_argument("--user", required=True, help="Neo4j Username")
parser.add_argument("--password", required=True, help="Neo4j Password")
parser.add_argument("--database", required=True, default="neo4j", help="Neo4j Database name")
parser.add_argument("--queries", nargs="*", help="List of Cypher queries")
parser.add_argument("--file", type=str, help="File containing Cypher queries")

args = parser.parse_args()

# Create Neo4j Connection
conn = Neo4jConnection(uri="neo4j://localhost:7687", user=args.user, pwd=args.password, db=args.database)

# Execute Queries
if args.file:
    with open(args.file, "r") as file:
        queries = [line.strip() for line in file if is_valid_cypher_query(line)]
        for query in queries:
            print(conn.query(query))
else:
    for query in args.queries:
        print(conn.query(query))

# Close Connection
conn.close()
