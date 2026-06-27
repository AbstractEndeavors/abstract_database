from .imports import *
class DbManager:
    def __init__(self, dbUrl=None):
        self.dbUrl = dbUrl or connectionManager().dburl

    def execute_query(self, query, params=None, fetch=False):
        """Executes a query on the database with optional parameters."""
        try:
            # Establish a connection to the database
            conn = psycopg.connect(self.dbUrl)
            cursor = conn.cursor(row_factory=dict_row)
            
            # Execute the query with parameters (if provided)
            cursor.execute(query, params)
            
            # Commit if it is a modifying query
            if not fetch:
                conn.commit()
                cursor.close()
                conn.close()
                return f"Query executed successfully: {query}"
            
            # Fetch results if requested (for SELECT queries)
            else:
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result

        except Exception as e:
            return f"An error occurred: {str(e)}"


# Function to handle user input queries
def query_input_function():

    print("Enter your SQL query (or type 'exit' to quit):")
    while True:
        # Get the user's query
        query = input("SQL> ")
        
        # Exit on 'exit' keyword
        if query.lower() == 'exit':
            break
        
        # Check if it is a SELECT query to fetch results
        fetch = query.strip().lower().startswith("select")
        
        # Execute the query
        result = DbManager().execute_query(query, fetch=fetch)
        
        # Print the results for SELECT queries
        if fetch:
            for row in result:
                print(row)
        else:
            print(result)
