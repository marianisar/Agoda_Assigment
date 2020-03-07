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
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, expose_headers='Authorization')
