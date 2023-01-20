import pymysql
import json
import collections
from datetime import datetime

def update(s):
    con = pymysql.connect(host='localhost', user='nemin', password='1234', db='face', charset='utf8')
    cur = con.cursor()

    sql = "select count(start) from faceInfo where start = %s;"
    cur.execute(sql, (datetime.today().strftime("%Y/%m/%d %H:%M:%S")))
    result = cur.fetchone()
    
    if(result[0] > 0):
        sql2 = "update faceInfo set name = %s where start = %s;"
        cur.execute(sql2, (s, datetime.today().strftime("%Y/%m/%d %H:%M:%S")))
        con.commit()
        con.close()
    else:
        sql2 = "insert into faceInfo (start, name) values (%s, %s);"
        cur.execute(sql2, (datetime.today().strftime("%Y/%m/%d %H:%M:%S"), s))
        con.commit()
        con.close()