#!/usr/bin/python3
#############################################################################
#                                                                           #
#                       Copyright 2020 Maria Nisar.                         #
#                           All Rights Reserved.                            #
#                                                                           #
# THIS WORK CONTAINS TRADE SECRET AND PROPRIETARY INFORMATION WHICH IS THE  #
#                   PROPERTY OF Maria Nisar                                 #
#                                                                           #
#############################################################################
'''
Module to Download Files.
@author: Maria Nisar
'''
import pymysql
from app import app
from db_config import mysql
from flask import jsonify


@app.route('/downloads')
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()
