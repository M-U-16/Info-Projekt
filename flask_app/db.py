import sqlite3
from datetime import datetime

def get_connection():
    conn = sqlite3.connect("wetter.db")
    return conn

def queryDb(query, args=[]):    
    conn = get_connection()
    cursor = conn.cursor()
    result = cursor.execute(query, args)
    conn.commit()
    return result

def addData(data):
    #date = data["time"]
    temp = data["temp"]
    humi = data["humi"]
    pres = data["pres"]
    lux = data["lux"]
        
    queryDb(
        "INSERT INTO wetterdaten(entry_date, entry_time, temp, humi, pres, lux) VALUES (?, ?, ?, ?, ?, ?)",
        (data["date"], data["time"], temp, humi, pres, lux)
    )
    
def getDay():
    currentDate = datetime.today().strftime('%Y-%m-%d')
        
    res = queryDb(
        "select * from wetterdaten where entry_date=?",
        [currentDate]
    ).fetchall()
    return res

def formatResponse(arr):
    newArr = []
    columns = [
        "entry_id", "entry_date",
        "entry_time", "temp",
        "humi",
        "pres",
        "lux",
        "high",
        "mid",
        "low",
        "amp",
        "oxi",
        "red",
        "nh3",
        "pm10",
        "pm25",
        "pm100"
    ]
    
    for entry in arr:
        dictonary = {}
        for index, value in enumerate(columns):
            dictonary[value] = entry[index]
        newArr.append(dictonary)
        
    return newArr