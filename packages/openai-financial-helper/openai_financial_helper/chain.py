from langchain_core.output_parsers import StrOutputParser
import sqlite3
import pandas as pd
import os
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.runnables import RunnableLambda

api_key = os.environ["OPENAI_API_KEY"]
current_directory = os.getcwd()
db_name = f"{current_directory}/records.db"
table_name = "financial_records"
csv_file = f"{current_directory}/expenses.CSV"

# Connect to database
conn = sqlite3.connect("records.db")
cursor = conn.cursor()

# Drop table to reset
drop_table_query = f"""DROP TABLE IF EXISTS  {table_name}"""
cursor.execute(drop_table_query)

# Create table
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        transaction_date TEXT,
        post_date TEXT,
        description TEXT,
        category TEXT,
        type TEXT,
        amount INTEGER,
        memo TEXT
    );
"""
cursor.execute(create_table_query)

# Read csv
df = pd.read_csv(csv_file, encoding="ISO-8859-1")
df.columns = [
    "transaction_date",
    "post_date",
    "description",
    "category",
    "type",
    "amount",
    "memo",
]

# Import the csv into database
df.to_sql(table_name, conn, if_exists="append", index=False)
conn.close()

# connect langchain to db
db = SQLDatabase.from_uri(f"sqlite:///{db_name}")
llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)


def get_schema(_):
    return db.get_table_info()


def run_query(s: str) -> str:
    return db_chain.run(s)

chain = RunnableLambda(func=run_query) | StrOutputParser()

# what was the most common category?
