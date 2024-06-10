import psycopg2
import os

dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

def insert_data(table_name, data):
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname,
            user,
            password,
            host,
            port=5432
        )
        # Create a cursor
        cur = conn.cursor()
        print("connnected")
        if 'session' in data:
            data['session'] = str(data['session'])
        
        # Construct the INSERT query
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Execute the query with data values
        cur.execute(query, list(data.values()))
        
        # Commit the transaction
        conn.commit()
        
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

def fetch_data(table_name, session):
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname,
            user,
            password,
            host,
            port=5432
        )
        # Create a cursor
        cur = conn.cursor()
        
        # Construct the SELECT query
        query = f"SELECT * FROM {table_name} WHERE session = %s"
        
        # Execute the query with data values
        cur.execute(query, (session,))
        
        # Fetch the data
        data = cur.fetchone()
        #check if active is true
        if not data[4]:
            return False
        return data
    except Exception as e:
        print(e)
        return False
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

def update_data(table_name, session, data):
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname,
            user,
            password,
            host,
            port=5432
        )
        # Create a cursor
        cur = conn.cursor()
        
        # Construct the UPDATE query
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"UPDATE {table_name} SET {columns} = {placeholders} WHERE session = %s"
        
        # Execute the query with data values
        cur.execute(query, list(data.values()) + [session])
        
        # Commit the transaction
        conn.commit()
        

        return True
    except Exception as e:
        return False
    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()