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

class LowaNonPublicSchool(Model):
    country_number = IntegerField(null=True)
    country_name = CharField(max_length=255, null=True)
    aea_number = IntegerField(null=True)
    district_number = IntegerField(null=True)
    school_number = IntegerField(null=True)
    school_name = CharField(max_length=255, null=True)
    school_level = IntegerField(null=True)
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
        table_name = 'iowa_non_public_school_scrape'

# pg_db.create_tables([LowaNonPublicSchool, ])

fp_read = xlrd.open_workbook("2018-2019 Iowa Non-Public School Building Directory.xlsx")
sh = fp_read.sheet_by_index(0)

school_level = {
	"6": "Nonpublic High School",
	"7": "Nonpublic Elementary School",
	"8": "Nonpublic K-12",
	"12": "Nonpublic System Office",
	"20": "Nonpublic Middle School"
}

for rx in range(1, sh.nrows):
    item = sh.row(rx)
    print item
    LowaNonPublicSchool.create(country_number=int(item[0].value),
            country_name=item[1].value,
            aea_number=checkData(item[2].value), district_number=int(item[3].value),
            school_number=int(item[4].value),
            school_name=item[5].value, 
            school_level=int(item[6].value), 
            po_box=item[7].value, 
            mailing_street=item[8].value, 
            mailing_city=item[9].value, 
            state=item[10].value, 
            zip=int(float(str(item[11].value).split("-")[0])), 
            physical_street=item[12].value, 
            physical_city=item[13].value, 
            physical_state=item[14].value, 
            physical_zip=int(float(str(item[15].value).split("-")[0])), 
            administrator_name=item[16].value, 
            administrator_title=item[17].value, 
            grade_start=item[18].value, 
            grade_end=item[19].value, 
            phone=item[20].value, 
            fax=item[21].value, 
            email=item[22].value, 
            created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")