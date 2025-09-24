from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        load_dotenv()
        uri = os.getenv("MONGO_URI")
        self.client = MongoClient(uri, 
                                server_api=ServerApi('1'),
                                tlsAllowInvalidCertificates=True)
        self.database = self.client.get_database("sample_mflix")
        self.movies = self.database.get_collection("movies")
        self.comments = self.database.get_collection("comments")
        self.users = self.database.get_collection("users")