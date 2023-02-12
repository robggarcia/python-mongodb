from pymongo import MongoClient

MONGODB_URI = 'mongodb+srv://yoshi:test123@cluster0.tvnuyyw.mongodb.net/?retryWrites=true&w=majority'

# set a 5-second connection timeout
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

for db_name in client.list_database_names():
    print(db_name)

db = client.get_database("bookstore")
