#!/usr/bin/python

import psycopg2
from pathlib import Path
from request_id_function import request_id

### Global variables ###

results=[]


### Database Connection ###

hostname = 'localhost'
username = 'postgres'
password = 'admin'
database = 'postgres'

conn = psycopg2.connect( host=hostname, user=username,
                         password=password, dbname=database )


cur = conn.cursor()


### Functions ###


def deleteContent(fName):
    with open(fName, "w"):
        pass



def recommend(*request):

    ### Local variables ###
    list_all=[]
    users_trust_found_3=[]
    users_trust_found_2=[]
    users_trust_found_1=[]

    request = tuple(request)

    params = {'request': request}

    ### Skills Match ###

    cur.execute("""SELECT skill_id,"Type" FROM "Skills"
        WHERE "Name" IN %(request)s """ ,params)

    rows = cur.fetchall()

    for row in rows:
        liste=[]
        skill_id = row[0]
        skill_type = row[1]
        if skill_type=='hard':
            cur.execute(""" SELECT user_id FROM "Profiles" WHERE skill_id='%s'
                 AND skill_level>=1 """ ,[skill_id])
        else:
            cur.execute(""" SELECT user_id FROM "Profiles"
                 WHERE skill_id='%s' AND skill_level=1 """ ,[skill_id])
        results=cur.fetchall()
        for result in results: liste.append(result[0])
        list_all.append(liste)

    users_found = list (set(list_all[0]).intersection(set(list_all[1])))

    ### Trust ###

                          ## High trust search ##

    cur.execute(""" SELECT user_id_dest FROM "Trust"
                   WHERE user_id_src='%s' AND trust_degree=3 """ ,[user_id_src])

    rows = cur.fetchall()

    if rows:
        for row in rows:
            users_trust_found_3.append(int(row[0]))

                           ## Mean trust search ##

    cur.execute(""" SELECT user_id_dest FROM "Trust"
                   WHERE user_id_src='%s' AND trust_degree=2 """ ,[user_id_src])

    rows = cur.fetchall()

    if rows:
        for row in rows:
            users_trust_found_2.append(int(row[0]))

                           ## Low trust search ##

    cur.execute(""" SELECT user_id_dest FROM "Trust"
                   WHERE user_id_src='%s' AND trust_degree=1 """ ,[user_id_src])

    rows = cur.fetchall()

    if rows:
        for row in rows:
            users_trust_found_1.append(int(row[0]))

    ### Users match ###

    users_match_most_trusted = list (set(users_found).intersection(set(users_trust_found_3)))
    
    users_match_meanly_trusted = list (set(users_found).intersection(set(users_trust_found_2)))
   
    users_match_less_trusted = list (set(users_found).intersection(set(users_trust_found_1)))
   

    return users_match_most_trusted,users_match_meanly_trusted,users_match_less_trusted

    conn.close()




### recommendation request ###

user='Carmine Bernard'    
user_id_src=request_id(user)

result=recommend('collaboration','génie logiciel','analyse de problème','leadership')

        ## Printing recommendation lists (organized by trust degree) ##
                      ## to a file for Gephi layout ##

recommendations = Path("C:\Python34")
if recommendations.is_file():
   deleteContent(f)
    
f = open('recommendations.txt','w+')

print(user,file=f)
for l in result:
    l=tuple(l)
    var = {'l': l}
    output=[]
    cur.execute(""" SELECT user_name FROM "Users"
               WHERE user_id IN %(l)s """ ,var)
    for i in cur.fetchall(): output.append(i[0])
    s = ", ".join(output)
    print(s,file=f)

f.close()

                 ## Collecting names into Gephi filter file ##

for l in result:
    for i in l: results.append(i)

results = tuple(results)
params = {'results': results}

cur.execute(""" SELECT user_name FROM "Users"
               WHERE user_id IN %(results)s """ ,params)

names = cur.fetchall()

Gephi_filter_file = Path("C:\Python34")
if Gephi_filter_file.is_file():
   deleteContent(f)
    
f = open('Gephi_filter_file.txt','w+')

print(user,file=f)
for n in names:
    print(n[0],file=f)

f.close()
