from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()   

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

class Neo4jGraph:
    def __init__(self):
        self.uri = URI
        self.auth = AUTH
        
    def create_user_node(self):
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            driver.verify_connectivity()

            def create_user_node(tx, user_id, username):
                tx.run("""
                    MERGE (u:User {
                        userID: $user_id,
                        username: $username
                    })
                """, user_id=user_id, username=username)

            def create_knows_relationship(tx, user1_id, user2_id):
                tx.run("""
                    MATCH (u1:User {userID: $user1_id})
                    MATCH (u2:User {userID: $user2_id}) 
                    MERGE (u1)-[:KNOWS]->(u2)
                """, user1_id=user1_id, user2_id=user2_id)

            def find_shortest_path(tx, start_id, end_id):
                result = tx.run("""
                    MATCH (start:User {userID: $start_id}),
                          (end:User {userID: $end_id}),
                          path = shortestPath((start)-[:KNOWS*]-(end))
                    RETURN [node IN nodes(path) | node.username] as usernames
                """, start_id=start_id, end_id=end_id)
                return result.single()["usernames"]

            # Create user nodes
            with driver.session() as session:
                with open('data/db_users.csv', 'r', encoding='utf-8') as f:
                    # Skip header
                    next(f)
                    for line in f:
                        id, username, *_ = line.strip().split(',')
                        session.execute_write(create_user_node, 
                                           int(id),
                                           username)

                # Create relationships
                with open('data/db_connections.csv', 'r', encoding='utf-8') as f:
                    # Skip header
                    next(f)
                    for line in f:
                        user1_id, user2_id = line.strip().split(',')
                        session.execute_write(create_knows_relationship,
                                           int(user1_id),
                                           int(user2_id))

                # Find shortest path from user 28 to 39
                path = session.execute_read(find_shortest_path, 28, 39)
                answer = ",".join(path)

            driver.close()

            print("--------------------------------")
            print("Shortest path:", answer)
            print("--------------------------------")

            return answer   