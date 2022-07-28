from ast import Import
from datetime import date, datetime
from random import random
import psycopg2
from configparser import ConfigParser

from regex import F
import qa_data_from_file
import random
import datetime

config_reader = ConfigParser()
config_reader.read("DB_Data/Profiles.ini")

user = 'postgres'


profile = config_reader[user]
name = profile['name']
password = profile['password']

conn = psycopg2.connect(
    database="PyQuiz",
    user=name,
    password=password,
    host="localhost",
    port="5432")
cur = conn.cursor()

recs_updated = {}

    
def update_db(table_name, file_name):
    results = qa_data_from_file.main(file_name)
    no_of_new_recs = 0
    no_of_recs_query = f'SELECT MAX(ID) FROM {table_name};'
    cur.execute(no_of_recs_query)
    result = cur.fetchall()
    if not result[0][0]:
        no_of_recs = 0
    else:
        no_of_recs = result[0][0]
# the following dictionary is for index and the QA data.so it will be like this {1:(Q,A),2:(Q,A)}
    data_set = {idx+1: data for idx, data in enumerate(list(results))}
    # since the index starts at 0, but the ids in the db start from 1 --> idx+1

    # for idx, data in data_set.items():
    #     print(idx)
    #     print(data)
    #     print()

    for idx, data in data_set.items():
        # %s is the placeholder in postgres, if this is not used, single quotes cause issue while running the query
        if idx > int(no_of_recs):
            syst_ef_ts = datetime.datetime.now()
            insert_query = f'INSERT INTO {table_name} VALUES (%s, %s, %s,%s,%s,%s);'
            if table_name in ('ETYMOLOGICAL_REFERENCES'):
                cur.execute(
                    insert_query, (idx, data[0][2:-2], data[1][1:-2], syst_ef_ts, "No","No"))
                conn.commit()
            elif table_name in ('PYTHON_DATA','PANDAS_DATA'):
                cur.execute(
                    insert_query, (idx, data[0][2:], data[1][2:-2], syst_ef_ts, "No","No"))
                conn.commit()

    no_of_new_recs = max(list(data_set.keys())) - no_of_recs
    recs_updated[table_name] = no_of_new_recs


# update_db()


def get_updated_recs(tables_to_be_updated):

    data_sources = {'PYTHON_DATA': 'Data.txt',
                    'PANDAS_DATA': 'Pandas_data.txt','ETYMOLOGICAL_REFERENCES':'Etymology.txt'}
    
    for table_name, file_name in data_sources.items():
        if table_name.lower() in tables_to_be_updated:
            update_db(table_name, file_name)

    conn.close()
    result = ''
    for table, num in recs_updated.items():
        if num:
            result += f'Table: {table} is updated with {num} new records \n'
        else:
            result += f'No new records are available for table: {table} \n'
    total_no = 0
    for nums in recs_updated.values():
        total_no += nums

    return result, total_no
