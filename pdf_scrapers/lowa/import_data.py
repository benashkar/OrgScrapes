import json
import time
import MySQLdb
from peewee import *
from time import gmtime, strftime

pg_db = MySQLDatabase('usa_raw', user='username', password='password',
                           host='db13.blockshopper.com', port=3306)        
pg_db.connect()

class LowaPost(Model):
    name = CharField(max_length=255, null=True)
    first_name = CharField(max_length=255, null=True)
    last_name = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    department = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'iowa_department_of_education_directory_scrape'

# pg_db.create_tables([LowaPost, ])

fp_read = open("data.txt", "rb")

for line in fp_read.readlines():
    if len(line.strip().split(" ")) < 2:
        continue

    item = dict()
    temp = line.strip().split(" ")
    print temp
    last_name = []
    index = 0
    for tp in temp:
        last_name.append(tp)
        index += 1
        if "," in tp:
            break
    item['last_name'] = " ".join(last_name).replace(",", "").strip()
    first_name = []
    for tp in temp[index:]:
        if "@" in tp:
            break
        first_name.append(tp)
        index += 1
    item['first_name'] = " ".join(first_name).strip()
    item['email'] = temp[index].strip()
    item['phone'] = temp[index+1].strip()
    item['department'] = " ".join(temp[index+2:]).strip()

    print json.dumps(item, indent=4)
    LowaPost.create(name="%s, %s" % (item['last_name'], item['first_name']),
            first_name=item['first_name'],
            last_name=item['last_name'], email=item['email'],
            phone=item['phone'],
            department=item['department'], 
            created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")
