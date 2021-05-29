#!/usr/bin/python3

from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class Graph:

    def __init__(self):
        uri = "bolt://localhost:7687"
        user = "neo4j"
        password = "password"

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_node(self, node_name, node_type):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_node, node_name, node_type)
            for row in result:
                print("Created [Node]: {p1}".format(p1=row['p1']))

    @staticmethod
    def _create_and_return_node(tx, node_name, node_type):
        # Create a query with given parameters and execute it
        query = (
            "CREATE (p1:{} ".format(node_type)+
                "{ name: $node_name }) "
            "RETURN p1"
        )
        result = tx.run(query, node_name=node_name)
        try:
            return [{"p1": row["p1"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_relationship(self, parent_node, parent_node_type, child_node, child_node_type, relationship_type):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_relationship, parent_node, parent_node_type, child_node, child_node_type, relationship_type)
            for row in result:
                print("Created [Relationship]: {parent} {relationship} {child}".format(parent=row["a"],relationship=row["r"] , child=row["b"]))

    @staticmethod
    def _create_and_return_relationship(tx, parent_node, parent_node_type, child_node, child_node_type, relationship_type):
        # Create a query with given parameters and execute it
        query = (
            "MATCH "
            "   (a:{}), ".format(parent_node_type)+
            "   (b:{}) ".format(child_node_type)+
            "WHERE a.name = $parent_node AND b.name = $child_node "
            "CREATE (a)-[r:{}]->(b) ".format(relationship_type)+
            "RETURN a,b,type(r) "
        )
        result = tx.run(query, parent_node=parent_node, child_node=child_node)
        try:
            return [{"a": row["a"]["name"], "b": row["b"]["name"], "r":row["type(r)"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_node(self, node_name, node_type):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_node, node_name, node_type)
            for row in result:
                print("Found [Node]: {row}".format(row=row))

    @staticmethod
    def _find_and_return_node(tx, node_name, node_type):
        # Create a query with given parameters and execute it
        query = (
            "MATCH (p:{}) ".format(node_type)+
            "WHERE p.name = $node_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, node_name=node_name)
        return [row["name"] for row in result]


def main():
    graph = Graph()
    graph.create_node("Shodan", "Class")
    graph.create_node("Request", "Support")
    graph.create_relationship("Shodan", "Class", "Request", "Support", "USES")
    graph.close()

if __name__ == "__main__":
   main()