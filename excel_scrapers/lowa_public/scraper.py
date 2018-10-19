import xlrd
import json
import time
import MySQLdb
from peewee import *
from time import gmtime, strftime

def checkData (val):
	try:
		val = int(val)
		return val
	except:
		return None

pg_db = MySQLDatabase('usa_raw', user='username', password='password',
                           host='db13.blockshopper.com', port=3306)    	
pg_db.connect()

class LowaPublicSchool(Model):
    country_number = IntegerField(null=True)
    country_name = CharField(max_length=255, null=True)
    aea_number = IntegerField(null=True)
    district_number = IntegerField(null=True)
    district_name = CharField(max_length=255, null=True)
    po_box = CharField(max_length=255, null=True)
    mailing_street = CharField(max_length=255, null=True)
    mailing_city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = IntegerField(null=True)
    physical_street = CharField(max_length=255, null=True)
    physical_city = CharField(max_length=255, null=True)
    physical_state = CharField(max_length=255, null=True)
    physical_zip = IntegerField(null=True)
    administrator_name = CharField(max_length=255, null=True)
    administrator_title = CharField(max_length=255, null=True)
    grade_start = CharField(max_length=255, null=True)
    grade_end = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    fax = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'iowa_public_school_district_scrape'

# pg_db.create_tables([LowaPublicSchool, ])

fp_read = xlrd.open_workbook("2018-2019 Iowa Public School District Directory.xlsx")
sh = fp_read.sheet_by_index(0)

for rx in range(1, sh.nrows):
    item = sh.row(rx)
    print item
    LowaPublicSchool.create(country_number=int(item[0].value),
            country_name=item[1].value,
            aea_number=checkData(item[2].value), district_number=int(item[3].value),
            district_name=item[4].value,
            po_box=item[5].value, 
            mailing_street=item[6].value, 
            mailing_city=item[7].value, 
            state=item[8].value, 
            zip=int(float(str(item[9].value).split("-")[0])), 
            physical_street=item[10].value, 
            physical_city=item[11].value, 
            physical_state=item[12].value, 
            physical_zip=int(float(str(item[13].value).split("-")[0])), 
            administrator_name=item[14].value, 
            administrator_title=item[15].value, 
            grade_start=item[16].value, 
            grade_end=item[17].value, 
            phone=item[18].value, 
            fax=item[19].value, 
            email=item[20].value, 
            created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")