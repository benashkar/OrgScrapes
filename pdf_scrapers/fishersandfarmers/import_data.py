import json
import time
import MySQLdb
from peewee import *
from time import gmtime, strftime

pg_db = MySQLDatabase('usa_raw', user='username', password='password',
                           host='db13.blockshopper.com', port=3306)        
pg_db.connect()

class FishingClub(Model):
    club_name = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    contact = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'fishing_club_city_scrape'

# pg_db.create_tables([FishingClub, ])

fp_read = open("data.txt", "rb")

for line in fp_read.readlines():
    item = dict()
    for state in [' IA ', ' NE ', ' IL ']:
        if state in line:
            item['state'] = state.strip()
            temp = line.split(state)
            temp = [temp[0], state.join(temp[1:])]
            break
    item['city'] = temp[0].strip()
    print temp
    temp = temp[1].split(" @@@ ")
    print temp
    item['club_name'] = temp[0]
    item['contact'] = temp[1]
    item['zip'] = temp[2].split(" ")[-1].strip()
    item['address'] = temp[2].replace(item['zip'], "").strip()

    print json.dumps(item, indent=4)
    FishingClub.create(club_name=item['club_name'],
            contact=item['contact'],
            address=item['address'], state=item['state'],
            zip=item['zip'],
            city=item['city'], 
            created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")
