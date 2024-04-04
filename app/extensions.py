from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# MongoDB configuration
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'github_events'
COLLECTION_NAME = 'events'

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

