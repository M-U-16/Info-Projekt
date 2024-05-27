import os
import sqlite3
from pathlib import Path
from os.path import join as path_join
from helpers.fakeEntrys import getManyRandomDataEntrys

""" def get_db():
    if "db" not in g:
        print(current_app.config) """

def getConnection(db_path):
    #create a connection to the sqlite db pass to it
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection
    
def create_all_tables(db_path, schema):
    con = getConnection(db_path)
    
    path_sql_files = path_join(Path(__file__).parent.absolute(), "schemas", schema)
    files = [f for f in os.listdir(path_sql_files)]
    file_paths = list(map(lambda f: path_join(path_sql_files, f), files))
    for path in file_paths:
        file = open(path, "r")
        con.executescript(file.read())
        file.close()
        
    con.commit()
    con.close()
    
def create_table(db_path, table_path):
    con = getConnection(db_path)
    
    file = open(table_path, "r")
    con.executescript(file.read())
    file.close()
    
    con.commit()
    con.close()

def random_populate_db(amount):
    con = getConnection(os.getenv("FLASK_WETTER_DATABASE_PATH"))
    
    data_general, data_gas = getManyRandomDataEntrys(amount)
    sql = generateSql(
        "insert into wetterdaten({}) values ({})",
        data_general[0].keys()
    )
    data_tuples = [tuple(entry.values()) for entry in data_general]
    chunk_size = 50
    for i in range(0, len(data_general), chunk_size):
        con.executemany(sql, data_tuples[i:i+chunk_size])
    
    data_gas_tuple = [tuple(entry.values()) for entry in data_gas]
    for i in range(0, len(data_gas), chunk_size):
        con.executemany("insert into gas(entry_date, oxi,red,nh3) values (?,?,?,?)", data_gas_tuple[i:i+chunk_size])
    
    con.commit()
    con.close()

def generateSql(sql_format, keys):
    columns_string = ""
    values_string = ""
    length = len(keys)
    for idx, i in enumerate(keys):
        columns_string += i + ("," if idx+1 != length else "")
        values_string += "?," if idx+1 != length else "?"
    return sql_format.format(columns_string, values_string)