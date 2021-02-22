import pymongo

client = pymongo.MongoClient("mongodb://admin:AAGzez02811@node9149-advweb-11.app.ruk-com.cloud:11154")
db = client["MMORPG"]

col = db["Character"]

doc = col.find_one()
print ("\nfind_one() result:", doc)