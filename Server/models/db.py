import os
import sqlite3
from dotenv import load_dotenv
#loading .env variables
load_dotenv()

DB_PATH = os.getenv("DATABASE_PATH")

querys = {
    "add-data": "INSERT INTO wetterdaten(entry_date, entry_time, temp, humi, pres, lux) VALUES (?, ?, ?, ?, ?, ?)",
    "current-day": "select * from wetterdaten where entry_date=Date('now')",
    "time-range": "select * from wetterdaten where entry_date between ? and ?",
    "get-week": "select * from wetterdaten where entry_date between DATE('now', '-7 days') and DATE('now')",
    "get-month":  "select * from wetterdaten where entry_date between DATE('now', '-1 month') and DATE('now')",
    "get-year": "select * from wetterdaten where entry_date between DATE('now', '-1 year') and DATE('now')",
}
columns = ["entry_id", "entry_date", "temp","humi", "pres","lux","noise", "oxi","red", "nh3","pm10", "pm25","pm100"]

def formatResponse(arr):
    newArr = []
    for entry in arr:
        dictonary = {}
        for index, value in enumerate(columns):
            dictonary[value] = entry[index]
        newArr.append(dictonary)
    return newArr

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    #conn.row_factory = sqlite3.Row
    return conn

#connection decorator
def connection(func):
    def func_wrapper(*args, **kwargs):
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        with connection:
            func(connection, cursor, *args, **kwargs)
    return func_wrapper

@connection
def test_query(conn, cur):
    cur.execute("select * from wetterdaten")
    rows = cur.fetchall()
    print(type(rows[0]))

def queryDb(query, args=[]):
    conn = get_connection()
    cursor = conn.cursor()
    result = cursor.execute(query, args).fetchall()
    conn.commit()
    conn.close()
    return result

def addData(data):
    data_tuple = (
        data["date"],
        data["time"],
        data["temp"],
        data["humi"],
        data["pres"],
        data["lux"]
    )
    queryDb( querys["add-data"], data_tuple)
    
def getDay():
    #currentDate = datetime.today().strftime('%Y-%m-%d')
    res = queryDb(querys["current-day"])
    return formatResponse(res)

def getTimeRange(firstDate, lastDate):
    res = queryDb(querys["time-range"], [firstDate, lastDate])
    return formatResponse(res)

def getWeek():
    res = queryDb(querys["get-week"])
    return formatResponse(res)

def getMonth():
    res = queryDb(querys["get-month"])
    return formatResponse(res)

def getYear():
    res = queryDb(querys["get-year"])
    print(res)
    return formatResponse(res)

def printAll():
    print(queryDb("select * from wetterdaten"))
    