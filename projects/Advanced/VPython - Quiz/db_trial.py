from random import random
import psycopg2
from configparser import ConfigParser
import random

config_reader = ConfigParser()
config_reader.read("DB_Data/Profiles.ini")

user = 'postgres'


profile = config_reader[user]
name = profile['name']
password = profile['password']


def main(no_of_qs):
    conn = psycopg2.connect(
        database="PyQuiz",
        user=name,
        password=password,
        host="localhost",
        port="5432")

########################################################################################################################
# select part
    cur = conn.cursor()
    # update_query = f"CREATE TABLE PYTHON_DATA LIKE LIKE QUIZ_DATA;"
    query = f"Select count(*) from PYTHON_DATA where to_be_revised = 'Yes' ;"
    # cur.execute(update_query)
    cur.execute(query)
    conn.commit()
    result = cur.fetchall()
    for item in result:
        print(item)

########################################################################################################################
# insert part

    # cur = conn.cursor()
    # query = 'TRUNCATE QUIZ_DATA;'
    # cur.execute(query)
    # conn.commit()
    # print('Done')


# list(map(str,ids_list))
main(5)
