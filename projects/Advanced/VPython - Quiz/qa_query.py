from random import random
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


def get_questions(no_of_qs, revision_flg,table_name,star_flg='No'):
    conn = psycopg2.connect(
        database="PyQuiz",
        user=name,
        password=password,
        host="localhost",
        port="5432")
    cur = conn.cursor()
    # first we get the ids of all the records with the given flag and then randomly chooses few among them
    if star_flg == 'Yes':
        query_records = f"Select id from {table_name} where to_be_revised = '{revision_flg}' and starred = '{star_flg}';"
    else:
        query_records = f"Select id from {table_name} where to_be_revised = '{revision_flg}';"


    cur.execute(query_records)
    available_recs_count = cur.fetchall()  # for one single result as tuple
    available_recs = [item[0] for item in available_recs_count]
    ids_list = random.sample(available_recs, k=no_of_qs)

    # if we use random.choices, it includes the repeated choices like 8,7,1,8 etc., to populate unique choices we are using
    # random.sample
    # query = 'Select * from noc_regions limit 10'
    if star_flg == 'Yes':
        query = f"select question,answer from {table_name} where id in {tuple(ids_list)} and to_be_revised = '{revision_flg}' and starred = '{star_flg}' order by id;"
    else:
        query = f"select question,answer from {table_name} where id in {tuple(ids_list)} and to_be_revised = '{revision_flg}' order by id;"
    cur.execute(query)

    result = cur.fetchall()
    conn.close()
    ids_list = sorted(ids_list) # to make sure the questions list and ids list are in sync
    return result, ids_list


# print(get_questions(3, 'Yes',"PYTHON_DATA",'No'))
