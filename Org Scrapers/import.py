import json
import time
import MySQLdb
from peewee import *
from time import gmtime, strftime

pg_db = MySQLDatabase('usa_raw', user='username', password='password',
                           host='db13.blockshopper.com', port=3306)    	
pg_db.connect()

class ElksPost(Model):
    lodge_name = CharField(max_length=255, null=True)
    lodge_number = IntegerField(null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    lodge_email = CharField(max_length=255, null=True)
    contact = CharField(max_length=255, null=True)
    website = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'elk_lodge_scrape'

class NationwidePost(Model):
    post_name = CharField(max_length=255, null=True)
    post_number = IntegerField(null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    contact_name = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    post_type = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'amvets_post_scrape'

class MoosePost(Model):
    lodge_name = CharField(max_length=255, null=True)
    lodge_number = IntegerField(null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    lodge_email = CharField(max_length=255, null=True)
    chapter_email = CharField(max_length=255, null=True)
    website = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'moose_lodge_scrape'

class NavyLeaguePost(Model):
    council_name = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    contact = CharField(max_length=255, null=True)
    website = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'navy_league_of_us_scrape'

class ArmyPost(Model):
    post_name = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    website = CharField(max_length=255, null=True)
    facebook = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'association_us_army_post_scrape'

class VeteransPost(Model):
    chapter_name = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    contact = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'national_association_for_black_veterans_scrape'

class AfaPost(Model):
    post_name = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    website = CharField(max_length=255, null=True)
    contact = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    post_type = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'afa_post_scrape'

class Iaumc(Model):
    org_name = CharField(max_length=255, null=True)
    physical_address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'iowa_UMC_scrape'

class Iowachamber(Model):
    chamber_name = CharField(max_length=255, null=True)
    director_name = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    website = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'iowa_chamebers_scrape'

class H4country(Model):
    office_name = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    website = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = '4_H_county_scrape'

class IowaRealtors(Model):
    name = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'iowa_realtors_scrape'

class Usavolleyballclubs(Model):
    club_name = CharField(max_length=255, null=True)
    website = CharField(max_length=255, null=True)
    contact = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    practice_area = CharField(max_length=255, null=True)
    club_type = CharField(max_length=255, null=True)
    player_age_range = CharField(max_length=255, null=True)
    club_volleyball_regoin = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'iowa_volleyball_club_scrape'

class Iahsaa(Model):
    school_name = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    state = CharField(max_length=255, null=True)
    zip = CharField(max_length=255, null=True)
    phone = CharField(max_length=255, null=True)
    principal_name = CharField(max_length=255, null=True)
    principal_phone = CharField(max_length=255, null=True)
    principal_email = CharField(max_length=255, null=True)
    athletic_administrator_name = CharField(max_length=255, null=True)
    athletic_administrator_phone = CharField(max_length=255, null=True)
    athletic_administrator_email = CharField(max_length=255, null=True)
    vice_principal_name = CharField(max_length=255, null=True)
    vice_principal_phone = CharField(max_length=255, null=True)
    vice_principal_email = CharField(max_length=255, null=True)
    website = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'iowa_hs_directory_scrape'

class IsdarModel(Model):
    chapter_name = CharField(max_length=255, null=True)
    city = CharField(max_length=255, null=True)
    address = CharField(max_length=255, null=True)
    website = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    created_by = CharField(max_length=255, null=True)
    created_date = CharField()
    updated_at = CharField()

    class Meta:
        database = pg_db
        table_name = 'iowa_dar_scrape'

pg_db.create_tables([IsdarModel, ])

def check(val):
    return None if val == "" else val
def clean(val):
    if val == None:
        return None
    val = ''.join([i if ord(i) < 128 else ' ' for i in val])
    return " ".join(val.split()).strip()

def importIsdar():
    fp = open("res_isdar.json", "rb")
    data = json.loads(fp.read())
    insert_data = []
    index = 1
    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        for key in item:
            item[key] = clean(check(item[key]))
        item['created_by'] = 'Ke'
        item['created_date'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        item['updated_at'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_data.append(item)
        index += 1

    IsdarModel.insert_many(insert_data).execute()

def importIahsaa():
    fp = open("res_iahsaa.json", "rb")
    data = json.loads(fp.read())
    insert_data = []
    index = 1
    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        for key in item:
            item[key] = clean(check(item[key]))
            if key in ['address', 'city']:
                item[key] = item[key].title()
        item['created_by'] = 'Ke'
        item['created_date'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        item['updated_at'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        insert_data.append(item)
        index += 1

    Iahsaa.insert_many(insert_data).execute()

def importUsavolleyballclubs():
    fp = open("res_usavolleyballclubs.json", "rb")
    data = json.loads(fp.read())
    insert_data = []
    index = 1
    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        address = item['address'].replace(",", "").strip() if item['address'][0] == "," else item['address']
        insert_data.append({'id': index, 'club_name': check(item['club_name']), 'website': check(item['website']), 'contact': check(item['contact']), 'email': clean(check(item['email'])), 'address': address, 'city': check(item['city']), 'state': check(item['state']).strip(), 'practice_area': check(item['practice_area']), 'club_type': check(item['club_type']), 'player_age_range': check(item['player_age_range']), 'club_volleyball_regoin': check(item['club _volleyball_regoin']), 'created_by': 'Ke', 'created_date': strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'updated_at': strftime("%Y-%m-%d %H:%M:%S", gmtime())})

        index += 1

    Usavolleyballclubs.insert_many(insert_data).execute()

def importIowaRealtors():
    fp = open("res_iowarealtors.json", "rb")
    data = json.loads(fp.read())
    insert_data = []
    index = 1
    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        insert_data.append({'id': index, 'name': check(item['name']), 'address': check(item['address']), 'city': check(item['city']), 'state': check(item['state']), 'zip': check(item['zip']), 'phone': check(item['phone']), 'email': check(item['email']), 'created_by': 'Ke', 'created_date': strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'updated_at': strftime("%Y-%m-%d %H:%M:%S", gmtime())})

        index += 1

    IowaRealtors.insert_many(insert_data).execute()

def importH4country():
    fp = open("res_h4country.json", "rb")
    data = json.loads(fp.read())

    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        H4country.create(office_name=item['county_name'].replace("county", "County") + " 4-H Office",
            address=item['address'].strip(), city=item['city'],
            state=item['state'], zip=item['zip'],
            phone=item['phone'], 
            website=item['website'],
            created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")

def importIowachamber():
    fp = open("res_iowachamber.json", "rb")
    data = json.loads(fp.read())

    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        Iowachamber.create(chamber_name=item['chamber_name'],
            director_name=item['director_name'], 
            address=item['address'], city=item['city'],
            state=item['state'], zip=item['zip'],
            email=item['email'],
            phone=item['phone'], 
            website=item['website'],
            created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")

def importElk():
    fp = open("res_elks.json", "rb")
    data = json.loads(fp.read())

    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        lodge_name = " ".join([item['lodge_name'].split(",")[0], "Elks Lodge", "No. " + item['lodge_name'].split("No. ")[1]])
        ElksPost.create(lodge_name=lodge_name,
            lodge_number=int(item['lodge_number']),
            address=item['address'], phone=item['phone'],
            lodge_email=item['email'],
            contact=item['contact'], created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            website=item['website'],
            created_by="Ke")

def updateElk():
    for elk in ElksPost.select().where(ElksPost.id>4942):
        address = elk.address.split(",")
        print address
        elk.city = address[1].strip()
        elk.state = address[2].strip().split(" ")[0]
        elk.zip = address[2].strip().split(" ")[1]
        elk.updated_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        elk.save()

def importNationwide():
    fp = open("res_nationwide.json", "rb")
    data = json.loads(fp.read())

    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        post_number = None if item['post_number'] == "" else int(item['post_number'])
        temp = "" if post_number == None else item['post_name'].split("Post ")[1]
        post_name = " ".join([item['post_name'].split(",")[0], "American Veterans Post", temp]).strip()
        NationwidePost.create(post_name=post_name,
            post_number=post_number,
            address=item['address'], contact_name=item['contact_name'],
            phone=item['phone'], post_type=item['post_type'],
            email=item['email'], created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")

def updateNationwide():
    for nationwide in NationwidePost.select():
        address = nationwide.address.split(",")
        print address
        nationwide.city = address[-2].strip()
        nationwide.state = address[-1].strip().split(" ")[0]
        nationwide.zip = address[-1].strip().split(" ")[1]
        nationwide.updated_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        nationwide.save()

def importMoose():
    fp = open("res_mooseintl.json", "rb")
    data = json.loads(fp.read())

    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        MoosePost.create(lodge_name=item['lodge_name'],
            lodge_number=int(item['lodge_number']),
            address=item['address'], phone=item['phone'],
            lodge_email=item['lodge_email'],
            chapter_email=item['chapter_email'],
            website=item['website'], created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")

def updateMoose():
    for moose in MoosePost.select().where(MoosePost.id>550):
        address = moose.address.split(",")
        print address
        moose.city = address[-2].strip()
        moose.state = address[-1].strip().split(" ")[0]
        moose.zip = address[-1].strip().split(" ")[1]
        moose.updated_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        moose.save()

def importNavyLeague():
    fp = open("res_navyleague.json", "rb")
    data = json.loads(fp.read())

    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        NavyLeaguePost.create(council_name="Navy League of the U.S %s Council" % item['council_name'],
            address=item['address'], email=item['email'],
            contact=item['contact'],
            website=item['website'], created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")

def updateNavyLeaguePost():
    for navy in NavyLeaguePost.select().where(NavyLeaguePost.id>429):
        address = navy.address.split(",")
        print address
        navy.city = address[0].strip()
        navy.state = address[1].strip()
        navy.zip = ""
        navy.updated_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        navy.save()

def importArmyPost():
    fp = open("res_ausa.json", "rb")
    data = json.loads(fp.read())

    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        ArmyPost.create(post_name=item['post_name'],
            address=item['address'], website=item['website'],
            facebook=item['facebook'], email=item['email'],
            phone=item['phone'], created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")

def updateArmyPost():
    for army in ArmyPost.select().where(ArmyPost.id>316):
        address = army.address.split(",")
        print address
        army.city = address[-3].strip()
        army.state = address[-2].strip().split(" ")[0].strip()
        try:
            army.zip = address[-2].strip().split(" ")[1].strip()
        except:
            army.zip = ""
        army.updated_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        army.save()

def importVeteransPost():
    fp = open("res_nabvets.json", "rb")
    data = json.loads(fp.read())

    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        VeteransPost.create(chapter_name=item['chapter_name'],
            address=item['address'], phone=item['phone'],
            contact=item['contact'], email=item['email'],
            created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")

def updateVeteransPost():
    for veteran in VeteransPost.select():
        if veteran.address == "":
            continue
        address = veteran.address.split(",")
        print address
        veteran.city = address[-2].strip()
        veteran.state = address[-1].strip().split(" ")[0].strip()
        try:
            veteran.zip = address[-1].strip().split(" ")[1].strip()
        except:
            veteran.zip = ""
        veteran.updated_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        veteran.save()

def importAfaPost():
    fp = open("res_afapost.json", "rb")
    data = json.loads(fp.read())

    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        AfaPost.create(post_name=item['post_name'],
            address=item['address'], website=item['website'],
            contact=item['contact'], email=item['email'],
            post_type=item['post_type'],
            created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")

def importIaumc():
    fp = open("res_iaumc.json", "rb")
    data = json.loads(fp.read())

    for item in data:
        print json.dumps(item, indent=4)
        timestamp = int(time.time())
        Iaumc.create(org_name=item['org_name'],
            physical_address=item['physical_address'], city=item['city'],
            state=item['state'], zip=item['zip'],
            email=item['email'],
            phone=item['phone'],
            created_date=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            updated_at=strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            created_by="Ke")

def updateAfaPost():
    for afa in AfaPost.select():
        if afa.address == "":
            continue
        address = afa.address.split(",")
        print address
        afa.city = address[0].strip()
        afa.state = address[1].strip()
        afa.zip = ""
        afa.updated_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        afa.save()

def updateZip():
    for item in ArmyPost.select():
        try:
            item.zip = item.zip.split("-")[0]
        except:
            item.zip = ""
        item.updated_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        item.save()

if __name__ == "__main__":
    importIsdar()
    # importH4country()
    # importIowachamber()