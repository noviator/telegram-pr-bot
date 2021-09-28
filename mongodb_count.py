import pymongo
from cred import Creds
from bson.objectid import ObjectId

connection_url = f"mongodb+srv://{Creds.mongo_db_username}:{Creds.mongo_db_password}@stats.y1p6x.mongodb.net/{Creds.databaseName}?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_url)

# database
db = client.get_database(Creds.databaseName)
# collection table
stats_table = db.allStats


def increaseCount(countString):
    counts = stats_table.find_one({'_id': ObjectId('6093fa8ddf4a80aad34___ddd1')})

    count_update = {
        countString: counts[countString] + 1
    }
    stats_table.update_one({'_id': ObjectId('6093fa8ddf4a80aad34___ddd1')}, {'$set': count_update})


def get_counts():
    return stats_table.find_one({'_id': ObjectId('6093fa8ddf4a80aad34___ddd1')})

# increaseCount('p_cmd')

# print(list(stats_table.find()))
