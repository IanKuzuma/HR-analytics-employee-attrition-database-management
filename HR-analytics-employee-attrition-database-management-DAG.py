"""
------------------------------------------------------------------------------------------------------------

Introduction

Name      : Ladityarsa Ilyankusuma
E-Mail    : ladityarsa.ian@gmail.com

Objective : This DAG orchestrates a simple but structured weekly data pipeline that fetches HR data from 
a PostgreSQL database, cleans and standardizes it, and then publishes it to Elasticsearch for further 
analysis and visualization in Kibana. The goal is to ensure that every Saturday morning, the latest cleaned 
data is consistently made available for decision-makers to monitor key employee metrics like attrition, 
travel behavior, and departmental stats, all without manual intervention.

Schedule  : Runs every Saturday at 09:10, 09:20, and 09:30 AM (GMT+7) to ensure timely updates and fallback 
redundancy in case of failure.

------------------------------------------------------------------------------------------------------------
"""

# Importing Libraries
import pandas as pd
import re
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from elasticsearch import Elasticsearch

# Define the DAG's default args
default_args= {
    'owner': 'Ian',
    'start_date': datetime(2024, 11, 1) - timedelta(hours=7),   # convert runtime log to GMT+7
    'retries': 1,                                               # rerun if there's a failed task 1 time
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG's parameters
with DAG(
    'P2M3_rd_ladityarsa_ilyankusuma_DAG',
    description='Sequential flow from PostgreSQL to Elasticsearch and Kibana',
    schedule_interval='10,20,30 9 * * 6',   # scheduled at minute 10, 20, and 30 past hour 9 on Saturday
    default_args=default_args, 
    catchup=False
) as dag:

    start = EmptyOperator(task_id='start')

    # === Task 1: Fetching the dataset from a postgresql database and inserting it to docker as a csv file ===
    @task()
    def fetch_from_postgresql():
        """
        This task function extracts raw data from a PostgreSQL table and saves it to a CSV file 
        in the local Airflow container.

        Args:
            None directly, but assumes:
                - A running PostgreSQL database named "airflow"
                - Accessible via host.docker.internal:5434
                - Table name: 'table_m3'

        Returns:
            None. Saves a CSV file to /opt/airflow/data/P2M3_rd_ladityarsa_ilyankusuma_data_raw.csv

        Example:
            # DAG execution
            fetch_from_postgresql()
        """

        database = "airflow"
        username = "airflow"
        password = "airflow"
        host = "host.docker.internal"
        port = "5434"

        postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

        engine = create_engine(postgres_url)
        conn = engine.connect()

        # Read the dataset from our airflow database using sql as df
        df = pd.read_sql('select * from table_m3', conn)

        # Save the raw dataset as a csv file
        df.to_csv('/opt/airflow/data/HR_employee_attrition_dataset_raw.csv', index=False)

        print("Inserting data is SUCCESS")

    # === Task 2: Preprocess the dataset such as duplicates handling and save it to a new csv file ===
    @task()
    def data_cleaning():
        """
        This task function cleans the dataset by removing duplicates, handling missing values, 
        and normalizing column names.
        Saves the cleaned dataset as a new CSV file.

        Args:
            None. Expects the raw CSV file to be present at:
                /opt/airflow/data/HR_employee_attrition_dataset_raw.csv

        Returns:
            None. Saves the cleaned dataset to:
                /opt/airflow/data/HR_employee_attrition_dataset_clean.csv

        Example:
            # DAG execution
            data_cleaning()
        """

        # Read the saved raw dataset csv file as df
        df = pd.read_csv('/opt/airflow/data/HR_employee_attrition_dataset_raw.csv')
        
        # Remove duplicates if any
        df.drop_duplicates(inplace=True)

        # Remove missing values if any
        df.dropna(inplace=True)

        # Reset dropped index
        df.reset_index(drop=True, inplace=True)

        # Normalize column names

        ## Create the function for normalizing the column names
        def normalize(col):
            """
            Normalizes column names by:
            - Stripping whitespaces
            - Replacing symbols/tabs with underscores
            - Inserting underscores between letters and numbers
            - Inserting underscores before uppercase letters
            - Removing redundant underscores
            - Lowercasing all characters

            Args:
                col (str): Original column name

            Returns:
                str: Normalized column name in snake_case

            Example:
                normalize(" ID ")               -> "id"
                normalize("numCompaniesWorked") -> "num_companies_worked"
                normalize("over18__")           -> "over_18"
                normalize("Monthly$Income")     -> "monthly_income"
            """

            col = col.strip()                                   # remove leading/trailing whitespace if any
            col = re.sub(r'[^A-Za-z0-9]', '_', col)             # replace symbols/tabs if any with underscore
            col = re.sub(r'(?<=[a-zA-Z])(?=[0-9])', '_', col)   # insert underscore between letters and digits
            col = re.sub(r'(?<=[0-9])(?=[a-zA-Z])', '_', col)   # insert underscore between digits and letters
            col = re.sub(r'(?<=[a-z])(?=[A-Z])', '_', col)      # insert underscore before uppercase letters
            col = re.sub(r'_+', '_', col)                       # collapse multiple underscores if any into one
            col = col.strip('_')                                # remove leading/trailing underscores if any
            col = col.lower()                                   # convert everything to lowercase for consistency
            return col                                          # return the celaned column name
        
        ## Dynamically normalize all column names using the function
        df.columns = [normalize(col) for col in df.columns]

        print("Preprocessing data is SUCCESS")
        print(df.head())

        # Save the cleaned dataset as a new csv file
        df.to_csv('/opt/airflow/data/HR_employee_attrition_dataset_clean.csv', index=False)

    # === Task 3: Secure a kibana connection with elasticsearch from our docker container for indexing ===
    @task()
    def post_to_elasticsearch():
        """
        Indexes each row of the cleaned dataset to Elasticsearch as individual JSON documents.

        Args:
            None. Reads from:
                /opt/airflow/data/HR_employee_attrition_dataset_clean.csv
            Assumes:
                - Elasticsearch running at http://elasticsearch:9200/
                - Target index: "index_m3"
                - doc_type: "doc"

        Returns:
            None. Prints Elasticsearch response for each row.

        Example:
            # DAG execution
            post_to_elasticsearch()
        """

        es = Elasticsearch(["http://elasticsearch:9200/"]) 

        # Read the saved clean dataset csv file as df
        df = pd.read_csv('/opt/airflow/data/HR_employee_attrition_dataset_clean.csv')

        # Convert the dataset to json and send it to elasticsearch
        for i, r in df.iterrows():
            doc=r.to_json()
            res=es.index(index="index_m3", doc_type="doc", body=doc)
            print(res)

    end = EmptyOperator(task_id='end')

    """
    Define the task sequence for the DAG using Airflow's bitshift operator (>>)
    
    Execution flow:
    1. `start`: EmptyOperator that marks the beginning of the DAG
    2. `fetch_from_postgresql()`: Extracts raw data from PostgreSQL and saves it to a CSV file
    3. `data_cleaning()`: Cleans the raw data (duplicates, missing values, and column normalization)
    4. `post_to_elasticsearch()`: Loads the cleaned data to Elasticsearch for Kibana indexing
    5. `end`: EmptyOperator that marks the end of the DAG execution
    
    This sequential flow ensures strict dependency enforcement between each ETL step
    """
    start >> fetch_from_postgresql() >> data_cleaning() >> post_to_elasticsearch() >> end