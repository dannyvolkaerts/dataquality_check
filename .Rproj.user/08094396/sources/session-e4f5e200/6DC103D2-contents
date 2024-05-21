import sqlite3
import pandas as pd
import os
import subprocess

# Step 1: Setup SQLite database and import dataset

# Connect to SQLite database. If the database does not exist, it will be created.
conn = sqlite3.connect('world_data.db')
cursor = conn.cursor()

# Create a table named 'cities' if it does not already exist.
# This table will store the uncleaned dataset with various columns for city information.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        city TEXT,
        city_ascii TEXT,
        lat REAL,
        lng REAL,
        country TEXT,
        iso2 TEXT,
        iso3 TEXT,
        admin_name TEXT,
        capital TEXT,
        population INTEGER,
        id INTEGER PRIMARY KEY
    );
""")

# Load data into the 'cities' table from a CSV file named 'worldcities.csv'.
# The DataFrame is read from the CSV file and then inserted into the SQL table.
df = pd.read_csv('worldcities.csv')
df.to_sql('cities', conn, if_exists='replace', index=False)

# Commit the changes to the database and close the connection.
conn.commit()
cursor.close()
conn.close()

# Step 2: Install and configure dbt

# Ensure the 'dbt_project' directory exists. This will be our working directory for the dbt project.
os.makedirs("dbt_project", exist_ok=True)

# Initialize a new dbt project named 'my_project' inside the 'dbt_project' directory.
# This command sets up the necessary directory structure and configuration files for dbt.
subprocess.run(["dbt", "init", "my_project"], cwd="dbt_project")

# Update the dbt profiles.yml file with SQLite connection details.
# The profiles.yml file contains connection details for various environments (e.g., dev, prod).
profiles_content = """
my_project:
  target: dev
  outputs:
    dev:
      type: sqlite
      path: world_data.db
      schema: main
      database: world_data.db
      schemas_and_paths:
        main: world_data.db
      schema_directory: dbt_project/my_project/schemas
"""

# Create the .dbt directory in the user's home directory if it doesn't already exist.
os.makedirs(os.path.expanduser("~/.dbt"), exist_ok=True)
# Write the SQLite connection configuration to the profiles.yml file.
with open(os.path.expanduser("~/.dbt/profiles.yml"), 'w') as f:
    f.write(profiles_content)

# Step 3: Create source declaration file
# In dbt, sources are external tables that dbt will read from. 
# We need to declare the 'cities' table as a source in dbt.

sources_yml_content = """
version: 2

sources:
  - name: main
    tables:
      - name: cities
"""

# Ensure the models directory exists in our dbt project.
os.makedirs("dbt_project/my_project/models", exist_ok=True)
# Write the source declaration to a YAML file inside the models directory.
with open("dbt_project/my_project/models/sources.yml", 'w') as f:
    f.write(sources_yml_content)

# Step 4: Create and run a dbt project
# dbt models are SQL files that contain transformation logic.
# We will create a model to clean the 'cities' data.

model_sql = """
WITH cleaned_data AS (
    SELECT
        city,
        city_ascii,
        lat,
        lng,
        country,
        iso2,
        iso3,
        admin_name,
        capital,
        population,
        id
    FROM
        {{ source('main', 'cities') }}
    WHERE
        population IS NOT NULL
        AND country != ''
        AND lat IS NOT NULL
        AND lng IS NOT NULL
)

SELECT
    *
FROM
    cleaned_data
"""

# Write the SQL model to a file inside the models directory.
with open("dbt_project/my_project/models/clean_cities.sql", 'w') as f:
    f.write(model_sql)

# Run the dbt project to execute the transformation.
# This will create a new view or table in the SQLite database based on the SQL model we defined.
subprocess.run(["dbt", "run"], cwd="dbt_project/my_project")
