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
from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'agoda'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Snx@D3fault'
app.config['MYSQL_DATABASE_DB'] = 'download'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
