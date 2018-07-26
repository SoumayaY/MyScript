#!/usr/bin/python

import psycopg2

def request_id(name):
    
    hostname = 'localhost'
    username = 'postgres'
    password = 'admin'
    database = 'postgres'

    conn = psycopg2.connect( host=hostname, user=username,
                         password=password, dbname=database )
    cur = conn.cursor()

    cur.execute(""" SELECT user_id FROM "Users"
               WHERE user_name=%s """ ,[name])

    user_id=cur.fetchone()[0]

    return (user_id)
