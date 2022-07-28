import psycopg2
from configparser import ConfigParser
import qa_data_from_file
import random

config_reader = ConfigParser()
config_reader.read("DB_Data/Profiles.ini")

user = 'postgres'


profile = config_reader[user]
name = profile['name']
password = profile['password']





def get_status(no_of_qs,table_name,key_word):
    conn = psycopg2.connect(
        database="PyQuiz",
        user=name,
        password=password,
        host="localhost",
        port="5432")
    cur = conn.cursor()
    if key_word == 'RANDOM_CHECK':
        query = f"Select count(*) from {table_name} where to_be_revised = 'No';"
    elif key_word == 'REVISION_CHECK':
        query = f"Select count(*) from {table_name} where to_be_revised = 'Yes';"
    elif key_word == 'STAR_CHECK':
        query = f"Select count(*) from {table_name} where starred = 'Yes';"
    cur.execute(query)
    available_recs_count = cur.fetchone()[0]  # for one single result as tuple
    conn.close()
    return  available_recs_count >= no_of_qs,available_recs_count



# print(check_rev_flgs(50,'PYTHON_DATA'))
