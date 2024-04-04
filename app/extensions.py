from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# MongoDB configuration
MONGO_URI = 'mongodb+srv://harshrajaeie24:YOwQSzQBKOOEjx76@cluster0.sszlr2n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
DB_NAME = 'github_events'
COLLECTION_NAME = 'events'

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

