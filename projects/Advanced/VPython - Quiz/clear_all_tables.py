import psycopg2
from configparser import ConfigParser
import random

config_reader = ConfigParser()
config_reader.read("DB_Data/Profiles.ini")

user = 'postgres'


profile = config_reader[user]
name = profile['name']
password = profile['password']




def delete_data():
    connector = psycopg2.connect(
        database="PyQuiz",
        user=name,
        password=password,
        host="localhost",
        port="5432")


    delete_queries  = ["DELETE FROM PYTHON_DATA;","DELETE FROM SQL_DATA;","DELETE FROM PANDAS_DATA;","DELETE FROM ETYMOLOGICAL_REFERENCES;"]
    select_queries  = ["SELECT COUNT(*) FROM PYTHON_DATA;","SELECT COUNT(*) FROM SQL_DATA;","SELECT COUNT(*) FROM PANDAS_DATA;","SELECT COUNT(*) FROM ETYMOLOGICAL_REFERENCES;"]
    with connector as conn:
        with conn.cursor() as curs:
            curs.execute(delete_queries[2]) # just give the index of the table above
            conn.commit()
            curs.execute(select_queries[2]) # just give the index of the table above
            result = curs.fetchone()
    
    print("Table dropped")
    print("result : ",result)
            
            # for query in queries:
            #     curs.execute(query)






delete_data()
