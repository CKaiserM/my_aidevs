import os
from dotenv import load_dotenv
from core.send_response import send_response_to_api_db, send_response
from core.openai_functions import generate_answer
load_dotenv()

def mission_12():
    """
    Mission 12 analyzes database tables and finds inactive datacenter managers.
    
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
    print("Mission 12 started")
    print("--------------------------------")

    # Get sample user data
    query = "SELECT * FROM users limit 1;"
    print("--------------------------------")
    whole_db = send_response_to_api_db(os.getenv("APIDB_URL"), "database", str(query))
    print("--------------------------------")
    print(whole_db)
    
    # Construct flag from ordered data
    print("--------------------------------")
    query = "SELECT * FROM correct_order ORDER BY weight;"
    print("--------------------------------")
    whole_db = send_response_to_api_db(os.getenv("APIDB_URL"), "database", str(query))
    print("--------------------------------")
    print(whole_db)
    flag = ""
    for table in whole_db.get("reply"):
        flag += table.get("letter")
    print("--------------------------------")
    print(flag)

    # Get connection information
    print("--------------------------------")
    query = "SELECT * FROM connections;"
    print("--------------------------------")
    whole_db = send_response_to_api_db(os.getenv("APIDB_URL"), "database", str(query))
    print("--------------------------------")
    print(whole_db)

    # Get and examine table structures
    print("--------------------------------")
    tables = "SHOW TABLES;"
    print("--------------------------------")
    print(tables)
    print("--------------------------------")
    tables_db = send_response_to_api_db(os.getenv("APIDB_URL"), "database", str(tables))
    print("--------------------------------")
    print(tables_db)
    print("--------------------------------")
    
    tables_details = []
    for table in tables_db.get("reply"):
        show_create_table = f"SHOW CREATE TABLE {table.get('Tables_in_banan')};"
        print(show_create_table)
        create_table_db = send_response_to_api_db(os.getenv("APIDB_URL"), "database", str(show_create_table))
        print(create_table_db)
        tables_details.append(create_table_db)

    # Generate and execute query for inactive datacenter managers
    user_prompt = str(tables_details)
    system_prompt = """    
        You are a helpful assistant that can answer questions and help with tasks.
        You are given a list of sql tables and their details.
        You need to answer the question based on the details of the tables.

        Write SQL query to get the data from the tables which will return DC_ID of only active datacenters whose managers (from the users table) are inactive.

        Very important: return only the raw SQL query text, without any additional descriptions, explanations, or Markdown formatting.
    """
    aiMessage = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    answer = generate_answer("gpt-4.1-mini", aiMessage)
    get_dc_id = send_response_to_api_db(os.getenv("APIDB_URL"), "database", str(answer))
    print(get_dc_id)
    
    # Process and report results
    dc_id = []
    for table in get_dc_id.get("reply"):
        dc_id.append(int(table.get("dc_id")))
    print(dc_id)
    response = send_response(os.getenv("RAPORT_URL"), "database", dc_id)
    
    print("--------------------------------")
    print("Mission 12 completed")
    print("--------------------------------")
    print("Response:", response)
