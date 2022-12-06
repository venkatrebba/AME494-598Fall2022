"""
Author: Venkatarao Rebba <rebba498@gmail.com>
This class intends to handle MongoDB Database
"""

from pymongo import MongoClient
import face_recognition
from datetime import datetime

class MongoDBHandler:
    def __init__(self) -> None:
        self.db_name = "test"
        self.collection_name = "registered_faces"
        self.db_connection = self.get_database()
        self.collection = self.db_connection[self.collection_name]
        
    def get_database(self):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = "mongodb://localhost:27017/myapp"
        
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)
        
        # Create the database for our example (we will use the same database throughout the tutorial
        return client[self.db_name]
    
    def get_records(self):
        persons = []
        face_embedding = []
        item_details = self.collection.find()
        for item in item_details:
            persons.append(item["Person"])
            face_embedding.append(item["embedding"])

        return persons, face_embedding

    def insert_sample_records(self):
        # Load a sample picture and learn how to recognize it.
        musk_image = face_recognition.load_image_file("musk1.jpeg")
        muskface_encoding = face_recognition.face_encodings(musk_image)[0]

        # Load a second sample picture and learn how to recognize it.
        trump_image = face_recognition.load_image_file("trump.png")
        trump_face_encoding = face_recognition.face_encodings(trump_image)[0]

        # Load a second sample picture and learn how to recognize it.
        venkat_image = face_recognition.load_image_file("venkat.png")
        venkat_face_encoding = face_recognition.face_encodings(venkat_image)[0]

        # Load a second sample picture and learn how to recognize it.
        venkat1_image = face_recognition.load_image_file("Venkat1.jpeg")
        venkat1_face_encoding = face_recognition.face_encodings(venkat1_image)[0]

        person1 = {
        # "_id" : "U1IT00001",
        "createdAt" : datetime.now(),
        "Person" : "Musk",
        "embedding" : muskface_encoding.tolist()
        }

        person2 = {
        # "_id" : "U1IT00001",
        "createdAt" : datetime.now(),
        "Person" : "Venkat",
        "embedding" : venkat1_face_encoding.tolist()
        }

        person3 = {
        "createdAt" : datetime.now(),
        "Person" : "Trump",
        "embedding" : trump_face_encoding.tolist()
        }

        person4 = {
        "createdAt" : datetime.now(),
        "Person" : "Venkat",
        "embedding" : venkat_face_encoding.tolist()
        }
        self.collection.insert_many([person1,person2, person3, person4])


    def insert_face_embedding(self, person, embedding):
        person_embedding = {
        "createdAt" : datetime.now(),
        "Person" : person,
        "embedding" : embedding.tolist()
        }
        self.collection.insert_one(person_embedding)


# if __name__ == "__main__":   
#     mangoDBHandler = MongoDBHandler()
#     mangoDBHandler.insert_sample_records()
#     data = mangoDBHandler.get_records()
#     print(data)
