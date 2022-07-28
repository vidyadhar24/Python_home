
import psycopg2
from configparser import ConfigParser
import qa_data_from_file
import random
import datetime

config_reader = ConfigParser()
config_reader.read("DB_Data/Profiles.ini")

user = 'postgres'


profile = config_reader[user]
name = profile['name']
password = profile['password']


def update_revision_flg(ids_list,table_name):
    conn = psycopg2.connect(
        database="PyQuiz",
        user=name,
        password=password,
        host="localhost",
        port="5432")

########################################################################################################################
    to_be_revised_flg = 'Yes'
    syst_ef_ts = datetime.datetime.now()

    cur = conn.cursor()
    update_query = f"UPDATE {table_name} SET TO_BE_REVISED = '{to_be_revised_flg}',syst_ef_ts = '{syst_ef_ts}' WHERE ID IN {tuple(ids_list)};"
    cur.execute(update_query)
    conn.commit()
    conn.close()


