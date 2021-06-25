#!/usr/bin/python3

from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from utils.support import Print

class Graph:
    def __init__(self):
        uri = "bolt://localhost:7687"
        user = "neo4j"
        password = "password"

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    # Create a node label (label = node_type)
    def create_node_label(self, existing_labels, new_label, node_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_node_label, existing_labels, new_label, node_name)
            for row in result:
                Print.dbPrint("CREATED ", "[DB-Node-Label]: {label} ({labels})".format(label=new_label, labels=", ".join(row["labels"])))

    @staticmethod
    def _create_and_return_node_label(tx, existing_labels, new_label, node_name):
        # Create a query with given parameters and execute it
        query = (
            "MATCH (n:{existing_labels}) ".format(existing_labels=existing_labels)+
            "WHERE n.name = $node_name "
            "SET n: {new_label} ".format(new_label=new_label)+
            "RETURN labels(n) AS labels"
        )
        result = tx.run(query, node_name=node_name)
        try:
            return [{"labels": row["labels"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    # Create a node
    def create_node(self, node_name, node_type):
        # pass
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_node, node_name, node_type)
            for row in result:
                Print.dbPrint("CREATED ", "[DB-Node]: {node}".format(node=row["p1"]))

    @staticmethod
    def _create_and_return_node(tx, node_name, node_type):
        # Create a query with given parameters and execute it
        query = (
            "CREATE (p1:{node_type} ".format(node_type=node_type)+
            "   { name: $node_name }) "
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

    # Create a relationship
    def create_relationship(self, parent_node, parent_node_type, child_node, child_node_type, relationship_type):
        # pass
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_relationship, parent_node, parent_node_type, child_node, child_node_type, relationship_type)
            for row in result:
                Print.dbPrint("CREATED ", "[DB-Relationship]: {parent} {relationship} {child}".format(
                    parent=row["a"],
                    relationship=row["r"] , 
                    child=row["b"]))

    @staticmethod
    def _create_and_return_relationship(tx, parent_node, parent_node_type, child_node, child_node_type, relationship_type):
        # Create a query with given parameters and execute it
        query = (
            "MATCH "
            "   (a:{parent_node_type}), ".format(parent_node_type=parent_node_type)+
            "   (b:{child_node_type}) ".format(child_node_type=child_node_type)+
            "WHERE a.name = $parent_node AND b.name = $child_node "
            "CREATE (a)-[r:{relationship_type}]->(b) ".format(relationship_type=relationship_type)+
            "RETURN a,b,type(r)"
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

    # Returns TRUE if found
    def find_node(self, node_name, node_type):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_node, node_name, node_type)
            
            if result:
                for row in result:
                    Print.dbPrint("FOUND ", "[DB-Node]: {row}".format(row=row))
                return True
            else:
                Print.dbErrorPrint("NOT FOUND ", "[DB-Node]: {node_name}".format(node_name=node_name))
                return False

    @staticmethod
    def _find_and_return_node(tx, node_name, node_type):
        # Create a query with given parameters and execute it
        query = (
            "MATCH (p:{node_type}) ".format(node_type=node_type)+
            "WHERE p.name = $node_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, node_name=node_name)
        return [row["name"] for row in result]

    # Return TRUE if found
    def find_relationship(self, parent_node, parent_node_type, child_node, child_node_type, relationship_type):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_relationship, parent_node, parent_node_type, child_node, child_node_type, relationship_type)
            
            if result:
                for row in result:
                    Print.dbPrint("FOUND ", "[DB-Relationship]: {parent_node} {relationship_type} {child_node}".format(
                            parent_node=parent_node,
                            relationship_type=row,
                            child_node=child_node
                        ))
                return True
            else:
                Print.dbErrorPrint("NOT FOUND ", "[DB-Relationship]: {parent_node} {relationship_type} {child_node}".format(
                        parent_node=parent_node,
                        relationship_type=relationship_type,
                        child_node=child_node
                    ))
                return False

    @staticmethod
    def _find_and_return_relationship(tx, parent_node, parent_node_type, child_node, child_node_type, relationship_type):
        # Create a query with given parameters and execute it
        query = (
            "MATCH (n:{parent_node_type})-[r:{relationship_type}]->(m:{child_node_type}) ".format(
                parent_node_type=parent_node_type,
                relationship_type=relationship_type,
                child_node_type=child_node_type
            )+
            "WHERE n.name = $parent_node and m.name = $child_node "
            "RETURN type(r)"
        )
        result = tx.run(query, parent_node=parent_node, child_node=child_node)
        return [row["type(r)"] for row in result]

def main():
    graph = Graph()
    # graph.create_node("TEST-1", "MY_NODE")
    # graph.create_node("Request", "Support")
    # graph.create_relationship("Shodan", "Class", "Request", "Support", "USES")
    # graph.find_node("Shodan", "Object")
    # graph.find_relationship("ShodanNotificationController", "CLASS", "Controller", "CLASS", "EXTENDS")
    graph.create_node_label("MY_NODE", "ANOTHER_LABEL", "TEST-1")
    graph.close()

if __name__ == "__main__":
   main()