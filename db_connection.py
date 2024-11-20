import pymongo

url = 'mongodb+srv://7597059486lg:MBzDgbEOSvapFomg@cluster0.kalu6.mongodb.net/fletnix?retryWrites=true&w=majority'
client  = pymongo.MongoClient(url , tls=True)
db = client['fletnix']