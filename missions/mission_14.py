import os
from dotenv import load_dotenv
from core.send_response import send_response_to_api_db, send_response
from core.misc import save_data_to_file, save_json_as_csv
import json
from core.graph_neo4j import Neo4jGraph

load_dotenv()

def mission_14():   
    """
    Mission 14 analyzes database tables and finds inactive datacenter managers.
    
    The function:
    1. Retrieves and displays basic database information
    2. Gets ordered data to construct a flag
    3. Examines database connections and table structures
    4. Uses GPT to generate a query finding datacenters with inactive managers
    5. Reports findings to an external service
    
    The function queries multiple database tables, constructs a flag from ordered data,
    and identifies datacenters where managers (from users table) are inactive.
    Results are sent to a reporting endpoint.
    """
    print("--------------------------------")
    print("Mission 14 started")
    print("--------------------------------")

    if os.path.exists("data/db_users.json") and os.path.exists("data/db_connections.json"):
        print("Data files already exist. Skipping database queries.")
        db_users = json.load(open("data/db_users.json"))
        db_connections = json.load(open("data/db_connections.json"))
        #save_json_as_csv(db_users, "data/db_users.csv")
        #save_json_as_csv(db_connections, "data/db_connections.csv")
    else:
        # Get sample user data
        query = "SELECT * FROM users;"
        print("--------------------------------")
        db_users = send_response_to_api_db(os.getenv("APIDB_URL"), "database", str(query))
        print("--------------------------------")
        print(db_users)
        print("--------------------------------")

        # Get sample user data
        query = "SELECT * FROM connections;"
        print("--------------------------------")
        db_connections = send_response_to_api_db(os.getenv("APIDB_URL"), "database", str(query))
        print("--------------------------------")
        print(db_connections)
        print("--------------------------------")

        save_data_to_file(db_users, "db_users", "data", ".json")
        save_data_to_file(db_connections, "db_connections", "data", ".json")

    graph = Neo4jGraph()
    answer = graph.create_user_node()
    print("--------------------------------")
    print("Shortest path:", answer)
    print("--------------------------------")
    response = send_response(os.getenv("RAPORT_URL"), "connections", answer)
    
    print("--------------------------------")
    print("Mission 14 completed")
    print("--------------------------------")
    print("Response:", response)
