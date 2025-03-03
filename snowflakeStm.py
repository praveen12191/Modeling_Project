import snowflake.connector

def execute_query_and_save_to_file(
    sql_query, 
    output_file, 
    snowflake_credentials
):
   
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=snowflake_credentials['user'],
            password=snowflake_credentials['password'],
            account=snowflake_credentials['account'],
            warehouse=snowflake_credentials['warehouse'],
            database=snowflake_credentials['database'],
            schema=snowflake_credentials['schema']
        )

        # Execute SQL query
        cursor = conn.cursor()
        cursor.execute(sql_query)

        # Fetch results
        rows = cursor.fetchall()

        # Save results to text file
        with open(output_file, 'w') as file:
            for row in rows:
                file.write('\t'.join(map(str, row)) + '\n')

        print(f"Query results saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# Snowflake credentials
snowflake_credentials = {
    'user': 'PRAVEEN.R@MRCOOPER.COM',
    'password': 'your_password',
    'account': 'your_account.snowflakecomputing.com',
    'warehouse': 'your_warehouse',
    'database': 'your_database',
    'schema': 'your_schema'
}

# SQL Query
sql_query = "SELECT * FROM your_table LIMIT 10;"

# Output file path
output_file = "query_results.txt"

# Run the function
execute_query_and_save_to_file(sql_query, output_file, snowflake_credentials)
