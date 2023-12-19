import mysql.connector
import json

# Specify the path to your JSON file
json_file_path = r'P:\Internship Assignment\Dashboard Migrate in Django\jsondata.json'

# Try opening the JSON file with different encodings
encodings_to_try = ['utf-8', 'utf-16', 'cp1252']  # You can add more if needed

for encoding in encodings_to_try:
    try:
        with open(json_file_path, 'r', encoding=encoding) as json_file:
            json_data = json.load(json_file)
        break  # If successful, break out of the loop
    except UnicodeDecodeError:
        continue  # Try the next encoding

# MySQL database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Internship"
)

# Create a cursor object to interact with the database
cursor = db_connection.cursor()

# Define the table name
table_name = "main_interndata"

# Check if the table exists
table_exists_query = f"SHOW TABLES LIKE '{table_name}'"
cursor.execute(table_exists_query)

if not cursor.fetchone():
    # Table doesn't exist, so create it
    create_table_query = """
        CREATE TABLE IF NOT EXISTS main_interndata (
            id INT AUTO_INCREMENT PRIMARY KEY,
            end_year VARCHAR(255),
            intensity INT,
            sector VARCHAR(255),
            topic VARCHAR(255),
            insight TEXT,
            url VARCHAR(512),
            region VARCHAR(255),
            start_year VARCHAR(255),
            impact VARCHAR(255),
            added VARCHAR(255),
            published VARCHAR(255),
            country VARCHAR(255),
            relevance INT,
            pestle VARCHAR(255),
            source VARCHAR(255),
            title TEXT,
            likelihood INT
        )
    """
    
    # Execute the table creation query
    cursor.execute(create_table_query)

# Define your JSON data insertion query (same as before)
insert_query = """
    INSERT INTO main_interndata (
        end_year, intensity, sector, topic, insight, url, region,
        start_year, impact, added, published, country, relevance,
        pestle, source, title, likelihood
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Insert data into the MySQL database
for item in json_data:
    # Handle empty 'end_year' and 'start_year' values
    end_year = int(item["end_year"]) if item["end_year"] else None
    start_year = int(item["start_year"]) if item["start_year"] else None

    # Handle missing 'likelihood' values
    if item["likelihood"] == "":
        likelihood = None  # Use None to represent missing data
    else:
        likelihood = int(item["likelihood"])  # Convert to integer

    # Handle missing 'intensity' values
    if item["intensity"] == "":
        intensity = None  # Use None to represent missing data
    else:
        intensity = int(item["intensity"])  # Convert to integer
    
    # Handle missing 'relevance' values
    if item["relevance"] == "":
        relevance = None  # Use None to represent missing data
    else:
        relevance = int(item["relevance"])  # Convert to integer


    data_values = (
        end_year, intensity, item["sector"], item["topic"],
        item["insight"], item["url"], item["region"], start_year,
        item["impact"], item["added"], item["published"], item["country"],
        relevance, item["pestle"], item["source"], item["title"],
        likelihood
    )
    cursor.execute(insert_query, data_values)

# Commit the changes and close the database connection
db_connection.commit()
db_connection.close()

print("Data inserted into the MySQL database successfully.")
