import os
import streamlit as st
import psycopg2
import pandas as pd
from uuid import uuid4


class DatabaseHandler:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        if "messages" not in st.session_state:
            st.session_state.messages = []
        st.session_state.db_uri = db_uri


        self.unique_id = str(uuid4()).replace("-", "_")
        self.connection = psycopg2.connect(self.db_uri)
        self.cursor = self.connection.cursor()
        self._create_data_folder()

    def _create_data_folder(self):
        if not os.path.exists('data'):
            os.makedirs('data')
            print("Folder 'data' created.")
        else:
            print("Folder 'data' already exists.")

    def get_basic_table_details(self):
        self.cursor.execute("""SELECT
                c.table_name,
                c.column_name,
                c.data_type
            FROM
                information_schema.columns c
            WHERE
                c.table_name IN (
                    SELECT tablename
                    FROM pg_tables
                    WHERE schemaname = 'public'
        );""")
        tables_and_columns = self.cursor.fetchall()
        return tables_and_columns

    def save_db_details(self):
        tables_and_columns = self.get_basic_table_details()
        df = pd.DataFrame(tables_and_columns, columns=['table_name', 'column_name', 'data_type'])
        filename_t = f'data/tables_{self.unique_id}.csv'
        df.to_csv(filename_t, index=False)
        self.cursor.close()
        self.connection.close()
        return self.unique_id
